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
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from mezzanine_instagram_gallery.models import InstagramUser

from instagram.client import InstagramAPI


def _get_instagram_api():
    client_id = settings.INSTAGRAM_CLIENT_ID
    client_secret = settings.INSTAGRAM_SECRET
    redirect = settings.INSTAGRAM_REDIRECT_URL
    return InstagramAPI(client_id=client_id, client_secret=client_secret,
                        redirect_uri=redirect)


def authorize(request):
    api = _get_instagram_api()
    scope = ['basic']
    redirect_uri = api.get_authorize_login_url(scope=scope)
    return HttpResponseRedirect(redirect_uri)


def callback(request):
    code = request.GET.get('code', '')
    if code:
        api = _get_instagram_api()
        token = api.exchange_code_for_access_token(code)
        info = token[1]
        users = InstagramUser.objects.filter(instagram_id=info['id'])
        if users:
            user = users[0]
            user.access_token = token[0]
        else:
            user = InstagramUser(access_token=token[0],
                                 instagram_id=info['id'],
                                 username=info['username'])
        user.save()
        return render_to_response('mezzanine_instagram_gallery/callback.html',
                                  dict(user=user),
                                  context_instance=RequestContext(request))
