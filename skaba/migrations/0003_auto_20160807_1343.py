# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-07 13:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('skaba', '0002_event_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
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
            model_name='userprofile',
            name='user',
        ),
        migrations.AddField(
            model_name='event',
            name='repeats',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='skaba.User'),
        ),
        migrations.AlterField(
            model_name='event',
            name='points',
            field=models.IntegerField(default=1),
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
