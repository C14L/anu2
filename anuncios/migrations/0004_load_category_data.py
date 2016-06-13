# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-13 11:06
from __future__ import unicode_literals

from django.db import migrations
from django.conf import settings
from django.utils.text import slugify

from anuncios.models import Category, Post


def add_category_data(apps, schema_editor):
    # Adds category data from settings.ANUNCIOS.CATEGORIES
    for cat in settings.ANUNCIOS['CATEGORIES']:
        if cat['parent'] is None:
            continue
        ncat = Category()
        ncat.slug = slugify(cat['slug'])
        ncat.old = cat['old']
        ncat.parent = slugify(cat['parent'])
        ncat.title = cat['title']
        ncat.descr = cat['descr']
        ncat.is_nsfw = cat.get('is_nsfw', True)
        ncat.save()


def remove_category_data(apps, schema_editor):
    Category.objects.all().delete()


def add_category_relations(apps, schema_editor):
    for post in Post.objects.all():
        try:
            cat = Category.objects.get(slug=post.category)
        except Category.DoesNotExist:
            continue
        post.categories.add(cat)


def remove_category_relations(apps, schema_editor):
    for post in Post.objects.all():
        post.categories.clear()


class Migration(migrations.Migration):

    dependencies = [
        ('anuncios', '0003_auto_20160613_1033'),
    ]

    operations = [
        migrations.RunPython(
            add_category_data,
            reverse_code=remove_category_data
        ),
        migrations.RunPython(
            add_category_relations,
            reverse_code=remove_category_relations
        ),
    ]
