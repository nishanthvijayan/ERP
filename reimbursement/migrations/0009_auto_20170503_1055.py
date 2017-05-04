# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-03 05:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reimbursement', '0008_auto_20170503_1043'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medical',
            name='transition_history',
        ),
        migrations.AddField(
            model_name='transitionhistory',
            name='medical',
            field=models.ForeignKey(help_text=b'Medical Reimbursement', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transition_history', to='reimbursement.Medical'),
        ),
        migrations.AlterField(
            model_name='medical',
            name='general_detail',
            field=models.ForeignKey(help_text=b'General Detail', on_delete=django.db.models.deletion.CASCADE, to='reimbursement.GeneralDetail'),
        ),
    ]