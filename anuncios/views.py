import os
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.http.response import HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.utils.translation import get_language
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, DetailView, CreateView, \
    UpdateView
from django.views.generic.base import View
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from anuncios.forms import PostForm
from anuncios.models import Post, Category
from anuncios.serializers import PostSerializer, UserSerializer
from anuncios.utils import get_category_item
from dtrcity.models import boundingBox, City, AltName


class HomeViewHTML(ListView):
    model = Category
    template_name = 'anuncios/home.html'

    def get_context_data(self, **kwargs):
        cats = settings.ANUNCIOS['CATEGORIES']
        context = super().get_context_data(**kwargs)
        context['city'] = City.get_by_url('mexico/puebla/puebla-de-zaragoza')
        context['grouping_list'] = [x for x in cats if x['parent'] is None]
        return context


class CategoryListHTML(ListView):
    model = Category

    def get_context_data(self, **kwargs):
        cats = settings.ANUNCIOS['CATEGORIES']
        context = super().get_context_data(**kwargs)
        context['city'] = City.get_by_url(self.kwargs['city'])
        context['grouping_list'] = [x for x in cats if x['parent'] is None]
        return context


class UserPostListHTML(ListView):
    """List of posts by a single user, usually 'own posts' for auth users."""
    paginate_by = 25
    template_name = 'anuncios/user_post_list.html'
    view_user = None

    def get_queryset(self):
        self.view_user = get_object_or_404(get_user_model(),
                                           pk=self.kwargs['user'])
        return Post.objects.by_user(self.view_user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_user'] = self.view_user
        return context


class PostListHTML(ListView):
    paginate_by = 25
    city = None
    category = None

    def get_queryset(self):
        self.city = City.get_by_url(self.kwargs['city'])
        self.category = get_object_or_404(Category,
                                          slug=self.kwargs['category'])
        return Post.objects.by_city_and_category(self.city, self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['city'] = self.city
        context['category'] = self.category
        return context


class PostCreateHTML(CreateView):
    model = Post
    form_class = PostForm

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        super().__init__(**kwargs)

    def get_initial(self):
        categories = self.request.GET.get('c', '').split(',')
        city_pk = self.request.GET.get('l', '')
        email = ''
        if self.request.user.is_authenticated():
            email = self.request.user.email

        return {
            'categories': Category.objects.filter(slug__in=categories),
            'city': get_object_or_404(City, pk=city_pk).pk,
            'created': now().strftime('%Y-%m-%d'),
            'publish': now().strftime('%Y-%m-%d'),
            'email': email,
        }

    def form_valid(self, form):
        if self.request.user.is_authenticated():
            form.instance.user = self.request.user
            form.instance.email = self.request.user.email
            form.instance.is_confirmed = True
            form.instance.is_public = True
        else:
            form.instance.email = form.cleaned_data['email'].strip().lower()
            form.instance.is_confirmed = False
            form.instance.is_public = True

        response = super().form_valid(form)
        return response

    def get_success_url(self):
        _args = [self.object.pk, self.object.slug]
        return reverse('post-detail-html', args=_args)


class PostDetailHTML(DetailView):
    model = Post
    object = None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.slug != self.kwargs['slug']:
            _args = [self.object.pk, self.object.slug]
            _url = reverse('post-detail-html', args=_args)
            return HttpResponsePermanentRedirect(_url)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        print('self.object.pk === {}'.format(self.object.pk))
        context = super().get_context_data(**kwargs)
        context['city'] = self.object.city
        return context


class PostUpdateHTML(UpdateView):
    model = Post
    form_class = PostForm

    def get_success_url(self):
        _args = [self.object.pk, self.object.slug]
        return reverse('post-detail-html', args=_args)
