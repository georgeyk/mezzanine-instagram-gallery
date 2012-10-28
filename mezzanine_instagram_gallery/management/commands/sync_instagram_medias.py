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

from django.conf import settings
from django.core.management.base import BaseCommand

from mezzanine.galleries.models import Gallery

from mezzanine_instagram_gallery.models import InstagramMedia


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        gallery_slug = settings.INSTAGRAM_GALLERIES[0][0]
        gallery = Gallery.objects.get(slug=gallery_slug)
        count = getattr(settings, 'INSTAGRAM_FETCH_COUNT', 20)
        for media in InstagramMedia.fetch_medias(count):
            media.save()
            media.to_mezzanine(gallery).save()

        for media in InstagramMedia.objects.filter(downloaded=False):
            media.to_mezzanine(gallery).save()
