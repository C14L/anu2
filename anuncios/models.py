import string
from datetime import timedelta, date
from uuid import uuid4

import random
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now
from imagekit.models import ProcessedImageField
from os.path import join
from pilkit.processors import ResizeToFit

from dtrcity.models import City


def get_image_path():
    return 'post-pictures/{0}/{1}'.format(date.today().year, str(uuid4()))


def make_username(email):
    return slugify(email).lower()[:30]


class Category(models.Model):
    slug = models.SlugField(blank=False)
    old = models.CharField(max_length=5, blank=True, default="")
    parent = models.CharField(max_length=20, blank=True, default="")
    title = models.CharField(max_length=50, blank=False)
    descr = models.CharField(max_length=500, blank=True, default="")
    is_nsfw = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile')


class PostQuerySet(models.QuerySet):

    def confirmed_only(self):
        return self.filter(is_confirmed=True)

    def by_user(self, user, include_unconfirmed=False):
        # user may be a pk, a username, or a User instance.
        if isinstance(user, int):
            user = User.objects.get(pk=user)
        elif isinstance(user, str):
            user = User.objects.get(username=user)

        if include_unconfirmed:
            return self.filter(user=user)

        return self.confirmed_only().filter(user=user)

    def by_city(self, city):
        # city may be a pk, a url, a crc, or a City instance.
        if isinstance(city, int):
            city = City.objects.get(pk=city)
        elif isinstance(city, str) and city.count(', ') == 2:
            city = City.get_by_url(city)
        elif isinstance(city, str) and city.count('/') == 2:
            city = City.get_by_crc(city)

        return self.confirmed_only().filter(city=city)

    def by_category(self, category):
        # category may be a pk, a slug, or a Category instance.
        if isinstance(category, int):
            category = Category.objects.get(pk=category)
        elif isinstance(category, str):
            category = Category.objects.get(slug=category)

        return self.confirmed_only().filter(categories=category)

    def by_city_and_category(self, city, category):
        return self.by_city(city).by_category(category)


class Post(models.Model):

    EXPIRE_DAYS = getattr(settings.ANUNCIOS, 'EXPIRE_DAYS', 90)
    CATEGORY_CHOICES = [(x['slug'], x['title']) for x in getattr(
        settings.ANUNCIOS, 'CATEGORIES', []) if x['parent'] != '']

    user = models.ForeignKey(User, db_index=True, null=True, default=None)

    categories = models.ManyToManyField(Category, related_name='posts')

    # TODO: remove, only used for import
    category = models.CharField(max_length=30, blank=True, default='',
                                db_index=True, choices=CATEGORY_CHOICES)

    lat = models.FloatField(null=True, default=None, blank=True)
    lng = models.FloatField(null=True, default=None, blank=True)

    # The city closest to the coords
    city = models.ForeignKey(City, null=True, default=None, blank=True,
                             related_name='posts')

    # The raw name strings for faster lookup
    city_name = models.CharField(max_length=100, default='', blank=True)
    region_name = models.CharField(max_length=100, default='', blank=True)
    country_name = models.CharField(max_length=100, default='', blank=True)

    title = models.CharField(max_length=200)  # for <h1> and <title>
    text = models.TextField()  # markdown

    pic_1 = ProcessedImageField(upload_to=get_image_path,
                                null=True, default=None, blank=True,
                                processors=[ResizeToFit(640, 640)],
                                format='JPEG', options={'quality': 70})
    pic_2 = ProcessedImageField(upload_to=get_image_path,
                                null=True, default=None, blank=True,
                                processors=[ResizeToFit(640, 640)],
                                format='JPEG', options={'quality': 70})
    pic_3 = ProcessedImageField(upload_to=get_image_path,
                                null=True, default=None, blank=True,
                                processors=[ResizeToFit(640, 640)],
                                format='JPEG', options={'quality': 70})
    pic_4 = ProcessedImageField(upload_to=get_image_path,
                                null=True, default=None, blank=True,
                                processors=[ResizeToFit(640, 640)],
                                format='JPEG', options={'quality': 70})

    created = models.DateTimeField(db_index=True, default=now, null=True, blank=True)
    updated = models.DateTimeField(default=now, null=True, blank=True)
    # auto-publish time:
    publish = models.DateTimeField(db_index=True, default=now, null=True, blank=True)
    expires = models.DateTimeField(default=None, null=True, blank=True)

    created_ip = models.CharField(max_length=30, default='', blank=True)
    updated_ip = models.CharField(max_length=30, default='', blank=True)

    # Secret PIN to edit anon posts.
    pin = models.CharField(max_length=5, default='', blank=True)
    # Times post was viewed.
    count_views = models.PositiveIntegerField(default=0, blank=True)
    # Times user updated post.
    count_updates = models.PositiveIntegerField(default=0, blank=True)
    # Times visitors send message through msg form.
    count_messages = models.PositiveIntegerField(default=0, blank=True)
    # Mark NSFW content.
    is_nsfw = models.BooleanField(default=False, blank=True)
    # Anonymous user has to confirm email via link before publication.
    is_confirmed = models.BooleanField(default=False, blank=True)
    # For the owner to temporarily un-publish an ad.
    is_public = models.BooleanField(default=False, blank=True)
    # For the owner or admin to delete an ad. Only admin can un-delete.
    is_delete = models.BooleanField(default=False, blank=True)

    class Meta:
        ordering = ['-pk']
        index_together = [['lat', 'lng'],
                          ['category', 'is_public', 'created'], ]

    objects = PostQuerySet.as_manager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.set_pin()
        if not self.expires:
            self.expires_days = 90
        super().save(*args, **kwargs)

    def set_pin(self):
        """Only set empty self.pin to a random string."""
        if not self.pin:
            ch = string.ascii_uppercase
            length = Post._meta.get_field('pin').max_length
            self.pin = ''.join(random.choice(ch) for _ in range(length))

    @property
    def expires_days(self):
        return (self.expires - now()).days

    @expires_days.setter
    def expires_days(self, days):
        if self.publish:
            self.expires = self.publish + timedelta(days=days)
        else:
            self.expires = now() + timedelta(days=days)

    @staticmethod
    def pic_from_base64(data, user, post):
        pic_path = join(settings.MEDIA_ROOT, 'pics')
        mimetype, pic_base64 = data.split(';base64,')
        mimetype = mimetype.replace('data:', '', 1)
        ext = mimetype.split('/')[1].lower().replace('jpeg', 'jpg')
        p = Pic.objects.create(user=user, post=post, ext=ext)
        fn = join(pic_path, '{}.{}'.format(p.id, ext))
        with open(fn, "wb") as fh:
            fh.write(pic_base64.decode('base64'))
        return p


class Inbox(models.Model):
    user = models.ForeignKey(User, db_index=True)         # receipient
    name = models.CharField(max_length=200, default='')   # req. sender name
    email = models.CharField(max_length=200, default='')  # opt. sender email
    phone = models.CharField(max_length=200, default='')  # opt. sender phone
    text = models.TextField(default='')                   # opt. message text
    created = models.DateTimeField(default=now)
    created_ip = models.CharField(max_length=30)
