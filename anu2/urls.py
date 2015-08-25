# -*- coding: utf-8 -*-
from __future__ import (unicode_literals, absolute_import, division,
                        print_function)

"""
------------------+-------------------+-------------------+-------------------+-------------------+
REST layout:      | GET               | POST              | PUT               | DELETE            |
------------------+-------------------+-------------------+-------------------+-------------------+
/posts/           | Show all posts    | Add new post      | Update all posts  | Delete all        |
/posts/<id>       | Show post <id>    | --                | Update post <id>  | Delete post <id>  |
                  |                   |                   |                   |                   |
                  |                   |                   |                   |                   |
                  |                   |                   |                   |                   |
                  |                   |                   |                   |                   |
------------------+-------------------+-------------------+-------------------+-------------------+

/guatemala/nacional/gente/mujer-busca-hombre.hb5

/nicaragua/managua/tema-gente.1

"""

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from anuncios import views
import dtrcity.urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^dtrcity/', include(dtrcity.urls)),

    url(r'^api/v1/users/$', 
        views.UserListAPIView.as_view(), name="user-item"),
    url(r'^api/v1/users/(?P<pk>[0-9]+)$', 
        views.UserItemAPIView.as_view(), name="user-list"),
    url(r'^api/v1/posts/$', 
        views.PostListAPIView.as_view(), name="post-list"),
    url(r'^api/v1/posts/(?P<pk>[0-9]+)/$', 
        views.PostItemAPIView.as_view(), name="post-item"),
    url(r'^api/v1/categories/$', 
        views.CategoriesListAPIView.as_view(), name="categories-list"),
    url(r'^api/v1/categories/(?P<pk>[a-z0-9-]+)/$', 
        views.CategoriesItemAPIView.as_view(), name="categories-item"),
    
    url(r'^.*$', views.AppHTMLView.as_view(), name="app"),
]

if not settings.PRODUCTION:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static('/pics/', document_root=settings.MEDIA_ROOT)
