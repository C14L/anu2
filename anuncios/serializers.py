from django.contrib.auth.models import User
from rest_framework import serializers

from anuncios.models import Post


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = (
          'id', 'user', 'category', 'lat', 'lng', 'title', 'text',
          'pic_1', 'pic_2', 'pic_3', 'pic_4',
          'created', 'updated', 'publish', 'expires',
          'count_views', 'count_updates', 'count_messages',
          'is_nsfw', 'is_public', 'is_delete'
        )


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
          'id', 'first_name', 'email', 'last_login', 'date_joined'
        )
