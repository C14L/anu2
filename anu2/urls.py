from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from anuncios import views, signals
import dtrcity.urls


"""
------------------+--------------+--------------+--------------+--------------+
REST layout:      | GET          | POST         | PUT          | DELETE       |
------------------+--------------+--------------+--------------+--------------+
/posts/           |show all posts|add new post  |upd.all posts |delete        |
/posts/<id>       |show post <id>|--            |upd.post <id> |del.post <id> |
                  |              |              |              |              |
------------------+--------------+--------------+--------------+--------------+

/guatemala/nacional/gente/mujer-busca-hombre.hb5
/nicaragua/managua/tema-gente.1

"""


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^dtrcity/', include(dtrcity.urls)),

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
