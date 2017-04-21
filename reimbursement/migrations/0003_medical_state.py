# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-21 09:17
from __future__ import unicode_literals

from django.db import migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('reimbursement', '0002_auto_20170421_0602'),
    ]

    operations = [
        migrations.AddField(
            model_name='medical',
            name='state',
            field=django_fsm.FSMField(blank=True, choices=[(1, b'Submitted by employee'), (2, b'Verified by Dealing Assistant'), (3, b'Approved by Medical Superintendent'), (4, b'Approved by Assistant Registrar'), (5, b'Approved by Deputy Registrar'), (6, b'Approved by Senior Audit Officer'), (7, b'Approved by Registrar'), (8, b'Amount transferred by Accounts Department')], default=1, max_length=50, protected=True),
        ),
    ]