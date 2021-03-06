# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-21 22:45
from __future__ import unicode_literals

import anuncios.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import imagekit.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Inbox',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=200)),
                ('email', models.CharField(default='', max_length=200)),
                ('phone', models.CharField(default='', max_length=200)),
                ('text', models.TextField(default='')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_ip', models.CharField(max_length=30)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(blank=True, db_index=True, default='', max_length=30)),
                ('lat', models.FloatField(default=None, null=True)),
                ('lng', models.FloatField(default=None, null=True)),
                ('title', models.CharField(max_length=200)),
                ('text', models.TextField(max_length='')),
                ('pic_1', imagekit.models.fields.ProcessedImageField(default=None, null=True, upload_to=anuncios.models.get_image_path)),
                ('pic_2', imagekit.models.fields.ProcessedImageField(default=None, null=True, upload_to=anuncios.models.get_image_path)),
                ('pic_3', imagekit.models.fields.ProcessedImageField(default=None, null=True, upload_to=anuncios.models.get_image_path)),
                ('pic_4', imagekit.models.fields.ProcessedImageField(default=None, null=True, upload_to=anuncios.models.get_image_path)),
                ('created', models.DateTimeField(db_index=True, default=django.utils.timezone.now, null=True)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('publish', models.DateTimeField(db_index=True, default=django.utils.timezone.now, null=True)),
                ('expires', models.DateTimeField(default=None, null=True)),
                ('created_ip', models.CharField(default='', max_length=30)),
                ('updated_ip', models.CharField(default='', max_length=30)),
                ('pin', models.CharField(default='', max_length=5)),
                ('count_views', models.PositiveIntegerField(default=0)),
                ('count_updates', models.PositiveIntegerField(default=0)),
                ('count_messages', models.PositiveIntegerField(default=0)),
                ('is_nsfw', models.BooleanField(default=False)),
                ('is_public', models.BooleanField(default=False)),
                ('is_delete', models.BooleanField(default=False)),
                ('user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterIndexTogether(
            name='post',
            index_together=set([('lat', 'lng'), ('category', 'is_public', 'created')]),
        ),
    ]
