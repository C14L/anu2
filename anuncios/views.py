import os
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import get_language
from django.views.generic.base import View
from rest_framework import generics
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
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


class CategoryList(APIView):

    def get(self, request):
        return Response({'location': {},
                         'categories': settings.ANUNCIOS['CATEGORIES']})


class CategoryDetail(APIView):

    def get(self, request, pk):
        return Response(get_category_item(pk))


class PostList(generics.ListCreateAPIView):
    """
    Return a list of matching posts. There are several filters that can be used
    to limit the number of posts returned. All requests require a category and
    category group defined.

    GET cgroup, category:
        Two string values, the "slug" of a category and it's parent.

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

    GET page:
        For pagination.
    """
    serializer_class = PostSerializer
    page_size = 10

    def get_queryset(self):
        city_id = self.request.query_params.get('city_id', None)
        city_url = self.request.query_params.get('city_url', None)
        lat = self.request.query_params.get('lat', None)
        lng = self.request.query_params.get('lng', None)
        dist = int(self.request.query_params.get('dist', 50))
        limit = int(self.request.query_params.get('limit', 100))
        lg = get_language()

        # Check for valid category.
        cgslug = self.request.query_params.get('cgroup', None)
        c_slug = self.request.query_params.get('category', None)

        try:
            category = [x for x in settings.ANUNCIOS['CATEGORIES']
                        if x['slug'] == c_slug][0]
        except IndexError:
            raise Http404

        # Check for valid parent (cgroup) category.
        try:
            cgroup = [x for x in settings.ANUNCIOS['CATEGORIES']
                      if x['slug'] == cgslug][0]
        except IndexError:
            raise Http404

        # Finally, check that cgroup is in fact the parent for category.
        if category['parent'] != cgroup['slug']:
            raise Http404

        # Still here? Then create an initial Queryset, then filter further by
        # geolocation.
        queryset = Post.objects.filter(category=category['slug'])

        if city_url:
            kw = {'url': city_url, 'language': lg, 'type': 3, 'is_main': True}
            city_id = get_object_or_404(AltName, **kw).geoname_id
        if city_id:
            city = get_object_or_404(City, pk=city_id)
            lat, lng = city.lat, city.lng
        if lat and lng:
            lat, lng = float(lat), float(lng)
            latmin, lngmin, latmax, lngmax = boundingBox(lat, lng, dist)
            queryset = queryset.filter(lat__gte=latmin, lng__gte=lngmin,
                                       lat__lte=latmax, lng__lte=lngmax)
        return queryset

    def create(self, request, *args, **kwargs):
        data = request.data['params']
        data['user'] = None
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        pic_urls = []
        if hasattr(data, 'pics') and isinstance(data['pics'], list):
            for pic in data['pics']:
                if pic:
                    p = Pic.create_from_base64(pic)
                    pic_urls.append(p.get_url())

        return Response([], status=status.HTTP_303_SEE_OTHER,
                        headers={'Location': '/'})


class PostDetail(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = PostSerializer
    model = serializer_class.Meta.model
    lookup_field = 'pk'  # default, added here only for verbosity.
    lookup_url_kwarg = 'pk'  # default, -"-
    queryset = Post.objects.all()

    # def get_queryset(self):
    #    print('THIS IS get_queryset() !')
    #    return Post.objects.filter(pk=self.kwargs['pk'])


class UserList(generics.ListCreateAPIView):

    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    page_size = 10


class UserDetail(generics.RetrieveUpdateDestroyAPIView):

    def get_queryset(self):
        return User.objects.get(pk=self.request.pk)
