import string
from datetime import timedelta, date
from uuid import uuid4

import random
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now
from imagekit.models import ProcessedImageField
from os.path import join
from pilkit.processors import ResizeToFit


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile')


def get_image_path():
    return 'post-pictures/{0}/{1}'.format(date.today().year, str(uuid4()))


class Post(models.Model):

    EXPIRE_DAYS = getattr(settings.ANUNCIOS, 'EXPIRE_DAYS', 30)
    CATEGORY_CHOICES = [(x['slug'], x['title']) for x in getattr(
        settings.ANUNCIOS, 'CATEGORIES', []) if x['parent'] != '']

    user = models.ForeignKey(User, db_index=True, null=True, default=None)

    category = models.CharField(max_length=30, blank=True, default='',
                                db_index=True, choices=CATEGORY_CHOICES)

    lat = models.FloatField(null=True, default=None)
    lng = models.FloatField(null=True, default=None)

    title = models.CharField(max_length=200)  # for <h1> and <title>
    text = models.TextField(max_length='')  # markdown

    pic_1 = ProcessedImageField(upload_to=get_image_path,
                                null=True, default=None,
                                processors=[ResizeToFit(640, 640)],
                                format='JPEG', options={'quality': 70})
    pic_2 = ProcessedImageField(upload_to=get_image_path,
                                null=True, default=None,
                                processors=[ResizeToFit(640, 640)],
                                format='JPEG', options={'quality': 70})
    pic_3 = ProcessedImageField(upload_to=get_image_path,
                                null=True, default=None,
                                processors=[ResizeToFit(640, 640)],
                                format='JPEG', options={'quality': 70})
    pic_4 = ProcessedImageField(upload_to=get_image_path,
                                null=True, default=None,
                                processors=[ResizeToFit(640, 640)],
                                format='JPEG', options={'quality': 70})

    created = models.DateTimeField(db_index=True, default=now, null=True)
    updated = models.DateTimeField(default=now, null=True)
    # auto-publish time:
    publish = models.DateTimeField(db_index=True, default=now, null=True)
    expires = models.DateTimeField(default=None, null=True)

    created_ip = models.CharField(max_length=30, default='')
    updated_ip = models.CharField(max_length=30, default='')

    # Secret PIN to edit anon posts.
    pin = models.CharField(max_length=5, default='')
    # Times post was viewed.
    count_views = models.PositiveIntegerField(default=0)
    # Times user updated post.
    count_updates = models.PositiveIntegerField(default=0)
    # Times visitors send message through msg form.
    count_messages = models.PositiveIntegerField(default=0)
    # Mark NSFW content.
    is_nsfw = models.BooleanField(default=False)
    # For the owner to temporarily un-publish an ad.
    is_public = models.BooleanField(default=False)
    # For the owner or admin to delete an ad. Only admin can un-delete.
    is_delete = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']
        index_together = [['lat', 'lng'],
                          ['category', 'is_public', 'created'], ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.set_pin()
        if not self.expires:
            self.expires_days(EXPIRE_DAYS)
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
