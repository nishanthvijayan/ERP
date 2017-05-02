# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-03 12:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reimbursement', '0024_auto_20170503_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transitionhistory',
            name='approved_by_group',
            field=models.ForeignKey(help_text=b'Employee Group', on_delete=django.db.models.deletion.CASCADE, to='auth.Group'),
        ),
    ]
