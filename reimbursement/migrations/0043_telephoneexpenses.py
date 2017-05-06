# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-05 17:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('erp_core', '0001_initial'),
        ('reimbursement', '0042_auto_20170505_1712'),
    ]

    operations = [
        migrations.CreateModel(
            name='TelephoneExpenses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('register_page_no', models.PositiveIntegerField(help_text=b'Enter page number of the register')),
                ('register_serial_no', models.PositiveIntegerField(help_text=b'Enter serial number for the record in the register')),
                ('amount_passed', models.DecimalField(decimal_places=2, help_text=b'Enter the amount passed for reimbursement', max_digits=8)),
                ('state', django_fsm.FSMField(blank=True, default=b'Submitted', max_length=50, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='telephone_expenses', to='erp_core.Employee')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]