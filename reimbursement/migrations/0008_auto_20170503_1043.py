# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-03 05:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reimbursement', '0007_auto_20170503_1041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medical',
            name='transition_history',
            field=models.ManyToManyField(help_text=b'Medical Reimbursement', to='reimbursement.TransitionHistory'),
        ),
    ]