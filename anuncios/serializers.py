# -*- coding: utf-8 -*-
from __future__ import (unicode_literals, absolute_import, division,
                        print_function)

from django.contrib.auth.models import User
from rest_framework import serializers
from anuncios.models import Post


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = (
          'id', 'user', 'category', 'lat', 'lng', 'title', 'text',
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
