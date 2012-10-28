# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

##
## Copyright (C) 2012 - George Y. Kussumoto <georgeyk.dev@gmail.com>
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.
##
##

import os.path
import time

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import models
from django.utils.translation import ugettext as _

from mezzanine.galleries.models import GalleryImage

from instagram.client import InstagramAPI

import requests


class InstagramUser(models.Model):
    instagram_id = models.CharField(max_length=64, blank=True, unique=True)
    username = models.CharField(max_length=64, blank=True)
    access_token = models.CharField(max_length=128)

    class Meta:
        verbose_name = _(u'Instagram User')
        verbose_name_plural = _(u'Instagram Users')

    def __unicode__(self):
        return u'InstagramUser: %s - %s' % (self.instagram_id, self.username)


class InstagramMedia(models.Model):
    instagram_id = models.CharField(max_length=128, unique=True)
    created = models.DateTimeField(blank=True)
    caption = models.CharField(max_length=256, blank=True)
    comment_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    url = models.URLField(blank=True)
    thumbnail_url = models.URLField()
    standard_url = models.URLField()

    downloaded = models.BooleanField(default=False)

    destination = 'uploads/instagram'

    class Meta:
        verbose_name = _(u'Instagram Media')
        verbose_name_plural = _(u'Instagram Medias')
        ordering = ('-created',)
        get_latest_by = 'created'

    def __unicode__(self):
        return u'InstagramMedia: %s - %s' % (self.instagram_id, self.caption)

    def _download_to(self, url, destination=''):
        if not destination:
            destination = self.destination
        filename = os.path.basename(url).decode('utf-8')

        downloaded_file = requests.get(url)
        if downloaded_file.ok:
            path = os.path.join(destination, filename)
            return default_storage.save(path,
                                        ContentFile(downloaded_file.content))

    #
    # Public API
    #

    def download_media(self, destination=''):
        assert self.standard_url
        return self._download_to(self.standard_url, destination)

    def download_media_thumbnail(self, destination=''):
        assert self.thumbnail_url
        return self._download_to(self.thumbnail_url, destination)

    def to_mezzanine(self, gallery, thumbnail=False):
        if thumbnail is False:
            downloaded_file = self.download_media()
        else:
            downloaded_file = self.download_media_thumbnail()
        if downloaded_file:
            self.downloaded = True
            self.save()

            return GalleryImage(gallery=gallery, description=self.caption,
                                file=downloaded_file)

    @classmethod
    def fetch_medias(cls, count):
        try:
            last_media = cls.objects.latest()
        except InstagramMedia.DoesNotExist:
            last_media = None

        min_time = ''
        if last_media:
            min_time = time.mktime(last_media.created.utctimetuple())

        user = InstagramUser.objects.all()[0]
        api = InstagramAPI(access_token=user.access_token)
        medias = api.user_recent_media(min_timestamp=min_time, count=count)
        if not (medias and medias[0]):
            raise StopIteration

        for media in medias[0]:
            if cls.objects.filter(instagram_id=media.id).exists():
                # TODO: check and update metadata
                continue

            caption = media.caption and media.caption.text or u''
            insta_media = cls(instagram_id=media.id,
                              created=media.created_time,
                              caption=caption,
                              comment_count=media.comment_count,
                              like_count=media.like_count,
                              url=media.link or u'',
                              thumbnail_url=media.images['thumbnail'].url,
                              standard_url=media.get_standard_resolution_url())
            yield insta_media
