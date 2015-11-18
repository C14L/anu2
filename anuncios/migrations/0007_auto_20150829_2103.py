# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import image_with_thumbnail_field


class Migration(migrations.Migration):

    dependencies = [
        ('anuncios', '0006_auto_20150829_2018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pic',
            name='pic',
            field=image_with_thumbnail_field.ImageWithThumbsField(default=None, null=True, upload_to='raw', blank=True),
        ),
    ]
