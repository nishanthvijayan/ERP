# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-10 01:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0004_delete_formelementtype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formelement',
            name='hint',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
