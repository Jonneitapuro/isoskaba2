# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-07 16:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skaba', '0003_auto_20160807_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
