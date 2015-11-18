# -*- coding: utf-8 -*-
from __future__ import (unicode_literals, absolute_import, division,
                        print_function)
import string
import random
from os.path import join
from datetime import timedelta  # datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now
# from image_with_thumbnail_field import ImageWithThumbsField

expire_days = getattr(settings.ANUNCIOS, 'EXPIRE_DAYS', 30)
pic_sizes = getattr(settings.ANUNCIOS, 'PIC_SIZES', (('s', 'cover', 75,  75),
                                                     ('m', 'cover', 300, 300),
                                                     ('x', 'contain', 800, 800)
                                                     ))


class Post(models.Model):

    CATEGORY_CHOICES = [(x['slug'], x['title']) for x in getattr(
        settings.ANUNCIOS, 'CATEGORIES', []) if x['parent'] != '']

    user = models.ForeignKey(User, db_index=True, null=True, default=None)
    # category has to have a parent main category!
    category = models.CharField(max_length=30, blank=True, default='',
                                db_index=True, choices=CATEGORY_CHOICES)
    lat = models.FloatField(null=True, default=None)
    lng = models.FloatField(null=True, default=None)
    title = models.CharField(max_length=200)  # for <h1> and <title>
    text = models.TextField(max_length='')  # markdown
    created = models.DateTimeField(db_index=True, default=now, null=True)
    updated = models.DateTimeField(default=now, null=True)
    # auto-publish time:
    publish = models.DateTimeField(db_index=True, default=now, null=True)
    expires = models.DateTimeField(default=None, null=True)
    created_ip = models.CharField(max_length=30, default='')
    updated_ip = models.CharField(max_length=30, default='')
    # Secret PIN to edit anon posts.
    pin = models.CharField(max_length=5, default='')
    # times post was viewed.
    count_views = models.PositiveIntegerField(default=0)
    # times user updated post.
    count_updates = models.PositiveIntegerField(default=0)
    # times visitors send message through msg form.
    count_messages = models.PositiveIntegerField(default=0)
    # mark NSFW content.
    is_nsfw = models.BooleanField(default=False)
    # only show when public.
    is_public = models.BooleanField(default=False)
    # mod or user deleted posts.
    is_delete = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']
        index_together = [['lat', 'lng'],
                          ['category', 'is_public', 'created'], ]

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.make_pin()
        if not self.expires:
            self.expires_days(expire_days)
        super(Post, self).save(*args, **kwargs)

    def expires_days(self, days=None):
        """Set self.expires if days are given. Return days until expires."""
        if days is None:
            return (self.expires - now()).days
        else:
            if self.publish:
                self.expires = self.publish + timedelta(days=days)
            else:
                self.expires = now() + timedelta(days=days)
            return days

    def make_pin(self):
        """Set empty(!) self.pin to a new random PIN."""
        if not self.pin:
            STRLEN = Post._meta.get_field('pin').max_length
            self.pin = ''.join(random.choice(string.ascii_uppercase)
                               for i in range(STRLEN))


class Inbox(models.Model):

    user = models.ForeignKey(User, db_index=True)  # receipient
    name = models.CharField(max_length=200, default='')  # req. sender name
    email = models.CharField(max_length=200, default='')  # opt. sender email
    phone = models.CharField(max_length=200, default='')  # opt. sender phone
    text = models.TextField(default='')  # opt. message text
    created = models.DateTimeField(default=now)
    created_ip = models.CharField(max_length=30)


class Pic(models.Model):

    user = models.ForeignKey(User, db_index=True, related_name='pics',
                             null=True, default=None)
    post = models.ForeignKey(Post, db_index=True, related_name='pics')
    # optional picture caption text
    text = models.TextField(blank=True, default='')
    # jpg gif png webp etc.
    ext = models.CharField(max_length=4, blank=True, default="")
    created = models.DateTimeField(default=now)
    created_ip = models.CharField(max_length=30, blank=True, default="")

    @classmethod
    def create_from_base64(data, user, post):
        pic_path = join(settings.MEDIA_ROOT, 'pics')
        mimetype, pic_base64 = data.split(';base64,')
        mimetype = mimetype.replace('data:', '', 1)
        ext = mimetype.split('/')[1].lower().replace('jpeg', 'jpg')
        p = Pic.objects.create(user=user, post=post, ext=ext)
        fn = join(pic_path, '{}.{}'.format(p.id, ext))
        with open(fn, "wb") as fh:
            fh.write(pic_base64.decode('base64'))
        return p

    def get_url(self):
        p = join(settings.MEDIA_ROOT, 'pics')
        f = '{}.{}'.format(self.id, self.ext)
        return join(p, f)
