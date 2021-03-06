# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-16 08:38
from __future__ import unicode_literals

import anuncios.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('anuncios', '0004_load_category_data'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-pk']},
        ),
        migrations.AddField(
            model_name='post',
            name='is_confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='city',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='dtrcity.City'),
        ),
        migrations.AlterField(
            model_name='post',
            name='count_messages',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='post',
            name='count_updates',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='post',
            name='count_views',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='post',
            name='created',
            field=models.DateTimeField(blank=True, db_index=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_ip',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='post',
            name='expires',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='lat',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='lng',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='pic_1',
            field=imagekit.models.fields.ProcessedImageField(blank=True, default=None, null=True, upload_to=anuncios.models.get_image_path),
        ),
        migrations.AlterField(
            model_name='post',
            name='pic_2',
            field=imagekit.models.fields.ProcessedImageField(blank=True, default=None, null=True, upload_to=anuncios.models.get_image_path),
        ),
        migrations.AlterField(
            model_name='post',
            name='pic_3',
            field=imagekit.models.fields.ProcessedImageField(blank=True, default=None, null=True, upload_to=anuncios.models.get_image_path),
        ),
        migrations.AlterField(
            model_name='post',
            name='pic_4',
            field=imagekit.models.fields.ProcessedImageField(blank=True, default=None, null=True, upload_to=anuncios.models.get_image_path),
        ),
        migrations.AlterField(
            model_name='post',
            name='pin',
            field=models.CharField(blank=True, default='', max_length=5),
        ),
        migrations.AlterField(
            model_name='post',
            name='publish',
            field=models.DateTimeField(blank=True, db_index=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='updated',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='updated_ip',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
    ]
