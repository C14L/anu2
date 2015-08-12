# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anuncios', '0002_auto_20150811_1008'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='classif',
            new_name='category',
        ),
        migrations.AddField(
            model_name='post',
            name='pin',
            field=models.CharField(default='', max_length=5),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_ip',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='post',
            name='updated_ip',
            field=models.CharField(default='', max_length=30),
        ),
    ]
