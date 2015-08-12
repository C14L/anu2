# -*- coding: utf-8 -*-
from __future__ import (unicode_literals, absolute_import, division,
                        print_function)

"""
REST layout:
------------------+-------------------+-------------------+-------------------+-------------------+
                  | GET               | POST              | PUT               | DELETE            |
------------------+-------------------+-------------------+-------------------+-------------------+
/posts/           | Show all posts    | Add new post      | Update all posts  | Delete all        |
/posts/<id>       | Show post <id>    | --                | Update post <id>  | Delete post <id>  |
                  |                   |                   |                   |                   |
                  |                   |                   |                   |                   |
                  |                   |                   |                   |                   |
                  |                   |                   |                   |                   |
------------------+-------------------+-------------------+-------------------+-------------------+

"""

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^api/v1/posts/$', 'anuncios.views.view_post_list'),
    url(r'^api/v1/posts/(?P<pk>[0-9]+)$', 'anuncios.views.view_post_item')
]

if not settings.PRODUCTION:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static('/pics/', document_root=settings.MEDIA_ROOT)
