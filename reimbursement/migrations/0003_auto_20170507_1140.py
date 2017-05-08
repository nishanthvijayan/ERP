# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-07 06:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reimbursement', '0002_auto_20170507_0145'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='medical',
            options={'verbose_name': 'Medical'},
        ),
        migrations.AlterModelOptions(
            name='telephoneexpense',
            options={'verbose_name': 'Telephone Expense'},
        ),
        migrations.AddField(
            model_name='billdetail',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, help_text=b'Amount mentioned on the bill', max_digits=10, null=True),
        ),
    ]
