# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('anuncios', '0004_auto_20150811_2025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='publish',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True, db_index=True),
        ),
        migrations.AlterIndexTogether(
            name='post',
            index_together=set([('category', 'is_public', 'created'), ('lat', 'lng')]),
        ),
    ]
