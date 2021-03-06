# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-25 17:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        ('forms', '0009_auto_20161123_1907'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transition',
            name='allowed_groups',
        ),
        migrations.AddField(
            model_name='state',
            name='allowed_groups',
            field=models.ManyToManyField(to='auth.Group'),
        ),
        migrations.AddField(
            model_name='transition',
            name='name',
            field=models.CharField(default='Default Name', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='workflow',
            name='allowed_groups',
            field=models.ManyToManyField(to='auth.Group'),
        ),
    ]
