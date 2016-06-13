from django.contrib import admin

from anuncios.models import Post, Category


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fields = ('categories', 'lat', 'lng', 'title', 'text',
              'created', 'updated', 'expires')


admin.site.register(Category)
