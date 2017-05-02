# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-03 10:57
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reimbursement', '0020_transitionhistory_approved_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transitionhistory',
            name='approved_by',
            field=models.ForeignKey(help_text=b'Employee', on_delete=django.db.models.deletion.CASCADE, related_name='transition_history', to=settings.AUTH_USER_MODEL),
        ),
    ]
