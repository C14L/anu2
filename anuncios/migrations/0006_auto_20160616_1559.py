# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-16 15:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('anuncios', '0005_auto_20160616_0838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='city',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='dtrcity.City'),
        ),
    ]
