# -*- coding: utf-8 -*-
from __future__ import (unicode_literals, absolute_import, division,
                        print_function)

import os
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
from django.views.generic.base import View, TemplateView
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from anuncios.models import Post
from anuncios.serializers import PostSerializer, UserSerializer
from anuncios.utils import get_category_item

class AppHTMLView(View):
    def get(self, request):
        fn = os.path.join(settings.BASE_DIR, "ng-app", "app.html")
        with open(fn, 'r') as fh:
            return HttpResponse(fh.read())

class CategoriesListAPIView(APIView):
    def get(self, request):
        res = {}
        res['categories'] = settings.ANUNCIOS.CATEGORIES
        res['location'] = { }
        return Response(res)

class CategoriesItemAPIView(APIView):
    def get(self, request, pk):
        return Response(get_category_item(pk))

class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    paginate_by = 10
    #permission_classes = (IsAdminUser,)
    #pagination_class = LargeResultsSetPagination

class PostItemAPIView(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return Post.objects.get(pk=self.request.pk)

class UserListAPIView(generics.ListCreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    paginate_by = 10

class UserItemAPIView(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return User.objects.get(pk=self.request.pk)
