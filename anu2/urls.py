from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

import dtrcity.urls
from anuncios import views, views_api


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^dtrcity/', include(dtrcity.urls)),

    # Web view
    # /guatemala/nacional/gente/mujer-busca-hombre.hb5
    # /nicaragua/managua/tema-gente.1

    url(r'^$',
        views.HomeViewHTML.as_view(), name='home-html'),

    url(r'^user/?$',
        views.UserListHTML.as_view(), name="user-list-html"),

    url(r'^user/(?P<pk>\d+)/?$',
        views.UserDetailHTML.as_view(), name="user-detail-html"),

    url(r'^clasificados/edit/(?P<pk>\d+)?$',
        views.PostUpdateHTML.as_view(), name="post-update-html"),

    url(r'^clasificados/(?P<pk>\d+)/(?P<slug>[-\w]+)/?$',
        views.PostDetailHTML.as_view(), name="post-detail-html"),

    url(r'^clasificados/?$',
        views.PostCreateHTML.as_view(), name="post-create-html"),

    # url(r'^clasificados/delete/(?P<pk>\d+)?$',
    #     views.PostDestroyHTML.as_view(), name="post-destroy-html"),

    url(r'^(?P<city>[-\w]+/[-\w]+/[-\w]+)/?$',
        views.CategoryListHTML.as_view(), name="category-list-html"),

    url(r'^(?P<city>[a-z0-9-_]+/[a-z0-9-_]+/[a-z0-9-_]+)/'
        r'(?P<category>[a-z0-9-_]+)/?$',
        views.PostListHTML.as_view(), name="post-list-html"),
]


"""urlpatterns += [
    url(r'^api/v1/users/$',
        views_api.UserList.as_view(), name="user-item"),
    url(r'^api/v1/users/(?P<pk>[0-9]+)$',
        views_api.UserDetail.as_view(), name="user-list"),
    url(r'^api/v1/posts/$',
        views_api.PostList.as_view(), name="post-list"),
    url(r'^api/v1/posts/(?P<pk>[0-9]+)/$',
        views_api.PostDetail.as_view(), name="post-item"),
    url(r'^api/v1/categories/$',
        views_api.CategoryList.as_view(), name="categories-list"),
    url(r'^api/v1/categories/(?P<pk>[a-z0-9-]+)/$',
        views_api.CategoryDetail.as_view(), name="categories-item"),
    url(r'^(?!p/|static/).*$',
        views_api.AppHTMLView.as_view(), name="app"),
]"""


if not settings.PRODUCTION:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static('/p/', document_root=settings.MEDIA_ROOT)
