# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-07 15:07
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('skaba', '0003_auto_20160807_1343'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=40, unique=True)),
                ('real_name', models.CharField(max_length=40)),
                ('is_tf', models.BooleanField(default=False)),
                ('is_kv', models.BooleanField(default=False)),
                ('role', models.CharField(default='user', max_length=8)),
                ('guild', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='skaba.Guild')),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='guild',
        ),
        migrations.AlterField(
            model_name='attendance',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
