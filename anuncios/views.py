# -*- coding: utf-8 -*-
from __future__ import (unicode_literals, absolute_import, division,
                        print_function)

import os

from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
from django.views.generic.base import View, TemplateView
from django.utils.translation import get_language

from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from anuncios.models import Post
from anuncios.serializers import PostSerializer, UserSerializer
from anuncios.utils import get_category_item

from dtrcity.models import boundingBox, City, AltName


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
    """Return a list of matching posts.

    There are several filters that can be used to limit the number of posts
    returned. 

    GET lat, lng, dist: 
        Return only posts geolocated within "dist" km from the 
        geolocation "lat/lng". This can be used to have users search
        for stuff in a certain distance from where they are, rather 
        than stuff within a certain named city.

    GET City.url, dist:
        Return only posts geolocated within "dist" km from the city 
        identified by the city's "url" value.

    GET City.id, dist:
        Same thing, but using the city's geoname_id.

    However, all requests require a category and category group defined.

    GET cgroup, category:
        Two string values, the "slug" of a category and it's parent.

    """

    def get_queryset(self):
        city_id = self.request.query_params.get('city_id', None)
        city_url = self.request.query_params.get('city_url', None)
        lat = self.request.query_params.get('lat', None)
        lng = self.request.query_params.get('lng', None)
        dist = int(self.request.query_params.get('dist', 50))
        lg = get_language()

        # Check for valid category.
        cgslug = self.request.query_params.get('cgroup', None)
        c_slug = self.request.query_params.get('category', None)
        try:
            category = [x for x in settings.ANUNCIOS.CATEGORIES 
                        if x['slug']==c_slug][0]
        except IndexError:
            raise Http404
        # Check for valid parent (cgroup) category.
        try:
            cgroup = [x for x in settings.ANUNCIOS.CATEGORIES 
                      if x['slug']==cgslug][0]
        except IndexError:
            raise Http404
        # Finally, check that cgroup is in fact the parent for category.
        if category['parent'] != cgroup['slug']:
            raise Http404

        # Still here? Then create an initial Queryset, then filter further by
        # geolocation.
        queryset = Post.objects.filter(category=category['title'])
        if city_url:
            kwargs = {'url':city_url, 'language':lg, 'type':3, 'is_main':True}
            city_id = get_object_or_404(AltName, **kwargs).geoname_id
        if city_id:
            city = get_object_or_404(City, pk=city_id)
            lat, lng = city.lat, city.lng
        if lat and lng:
            lat, lng = float(lat), float(lng)
            latmin, lngmin, latmax, lngmax = boundingBox(lat, lng, dist)
            queryset = queryset.filter(lat__gte=latmin, lng__gte=lngmin,
                                       lat__lte=latmax, lng__lte=lngmax)
        return queryset

    serializer_class = PostSerializer
    paginate_by = 100
    #permission_classes = (IsAdminUser,)
    #pagination_class = LargeResultsSetPagination

class PostItemAPIView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = PostSerializer
    model = serializer_class.Meta.model
    lookup_field = 'pk' # default, added here only for verbosity.
    lookup_url_kwarg = 'pk' # default, -"-
    queryset = Post.objects.all()
    #def get_queryset(self):
    #    print('THIS IS get_queryset() !')
    #    return Post.objects.filter(pk=self.kwargs['pk'])

class UserListAPIView(generics.ListCreateAPIView):

    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    paginate_by = 10

class UserItemAPIView(generics.RetrieveUpdateDestroyAPIView):

    def get_queryset(self):
        return User.objects.get(pk=self.request.pk)
