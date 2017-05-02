# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-03 13:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reimbursement', '0031_auto_20170503_1905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transitionhistory',
            name='medical',
            field=models.ForeignKey(help_text=b'Medical', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transition_history_medical', to='reimbursement.Medical'),
        ),
    ]
