# -*- coding: utf-8 -*-
from __future__ import (unicode_literals, absolute_import, division,
                        print_function)

import string
import random
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now
from image_with_thumbnail_field import ImageWithThumbsField

expire_days = getattr(settings.ANUNCIOS, 'EXPIRE_DAYS', 30)
pic_sizes = getattr(settings.ANUNCIOS, 'PIC_SIZES', (('s', 'cover', 75,  75),
                                                     ('m', 'cover', 300, 300),
                                                     ('x', 'contain', 800, 800)
                                                    ))
category_choices = [(x['slug'], x['title']) for x in getattr(
        settings.ANUNCIOS, 'CATEGORIES', []) if x['parent'] != '']

class Post(models.Model):

    user = models.ForeignKey(User, db_index=True)
    category = models.CharField( # These have to have a parent main category!
        max_length=30, blank=True, default='', db_index=True,
        choices=category_choices)
    lat = models.FloatField(null=True, default=None)
    lng = models.FloatField(null=True, default=None)
    title = models.CharField(max_length=200) # for <h1> and <title>
    text = models.TextField(max_length='') # Markdown
    created = models.DateTimeField(db_index=True, default=now, null=True)
    updated = models.DateTimeField(default=now, null=True)
    publish = models.DateTimeField(db_index=True, default=now, null=True) # auto-publish time
    expires = models.DateTimeField(default=None, null=True)
    created_ip = models.CharField(max_length=30, default='')
    updated_ip = models.CharField(max_length=30, default='')
    pin = models.CharField(max_length=5, default='') # Secret PIN to edit anon posts.
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

    user = models.ForeignKey(User, db_index=True)      # receipient
    name = models.CharField(max_length=200, default='')     # req. sender name
    email = models.CharField(max_length=200, default='')    # opt. sender email
    phone = models.CharField(max_length=200, default='')    # opt. sender phone
    text = models.TextField(default='')                     # opt. message text
    created = models.DateTimeField(default=now)
    created_ip = models.CharField(max_length=30)

class Pic(models.Model):

    user = models.ForeignKey(User, db_index=True, related_name='pics')
    post = models.ForeignKey(Post, db_index=True, related_name='pics')
    pic = ImageWithThumbsField(blank=False, upload_to='raw', sizes=(pic_sizes))
    text = models.TextField(default='')                     # opt. pic. caption
    created = models.DateTimeField(default=now)
    created_ip = models.CharField(max_length=30)

