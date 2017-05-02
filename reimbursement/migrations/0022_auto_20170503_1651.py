# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-03 11:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reimbursement', '0021_auto_20170503_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transitionhistory',
            name='approved_by',
            field=models.ForeignKey(help_text=b'Employee', on_delete=django.db.models.deletion.CASCADE, related_name='transition_history_approved_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='transitionhistory',
            name='medical',
            field=models.ForeignKey(help_text=b'Medical', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transition_history_medical', to='reimbursement.Medical'),
        ),
        migrations.AlterField(
            model_name='transitionhistory',
            name='transition',
            field=models.ForeignKey(help_text=b'Transition', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transition_history_transition', to='reimbursement.Transition'),
        ),
    ]
