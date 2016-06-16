from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

import dtrcity.urls
from anuncios import views

"""
------------------+--------------+--------------+--------------+--------------+
REST layout:      | GET          | POST         | PUT          | DELETE       |
------------------+--------------+--------------+--------------+--------------+
/posts/           |show all posts|add new post  |upd.all posts |delete        |
/posts/<id>       |show post <id>|--            |upd.post <id> |del.post <id> |
                  |              |              |              |              |
------------------+--------------+--------------+--------------+--------------+


"""


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^dtrcity/', include(dtrcity.urls)),

    # Web view
    # /guatemala/nacional/gente/mujer-busca-hombre.hb5
    # /nicaragua/managua/tema-gente.1

    url(r'^$',
        views.HomeViewHTML.as_view(), name='home-html'),

    url(r'^clasificados/user/(?P<pk>\d+)/?$',
        views.UserPostListHTML.as_view(), name="user-post-list-html"),

    url(r'^clasificados/edit/(?P<pk>\d+)?$',
        views.PostUpdateHTML.as_view(), name="post-update-html"),

    url(r'^clasificados/(?P<pk>\d+)/?$',
        views.PostDetailHTML.as_view(), name="post-detail-html"),

    url(r'^clasificados/?$',
        views.PostCreateHTML.as_view(), name="post-create-html"),

    # url(r'^clasificados/del/(?P<pk>\d+)?$',
    #     views.PostDestroyHTML.as_view(), name="post-destroy-html"),

    url(r'^(?P<city>[-\w]+/[-\w]+/[-\w]+)/?$',
        views.CategoryListHTML.as_view(), name="category-list-html"),

    url(r'^(?P<city>[a-z0-9-_]+/[a-z0-9-_]+/[a-z0-9-_]+)/'
        r'(?P<category>[a-z0-9-_]+)/?$',
        views.PostListHTML.as_view(), name="post-list-html"),

    # ---

    url(r'^api/v1/users/$',
        views.UserList.as_view(), name="user-item"),
    url(r'^api/v1/users/(?P<pk>[0-9]+)$',
        views.UserDetail.as_view(), name="user-list"),

    url(r'^api/v1/posts/$',
        views.PostList.as_view(), name="post-list"),
    url(r'^api/v1/posts/(?P<pk>[0-9]+)/$',
        views.PostDetail.as_view(), name="post-item"),

    url(r'^api/v1/categories/$',
        views.CategoryList.as_view(), name="categories-list"),
    url(r'^api/v1/categories/(?P<pk>[a-z0-9-]+)/$',
        views.CategoryDetail.as_view(), name="categories-item"),

    url(r'^.*$', views.AppHTMLView.as_view(), name="app"),
]


if not settings.PRODUCTION:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static('/pics/', document_root=settings.MEDIA_ROOT)
