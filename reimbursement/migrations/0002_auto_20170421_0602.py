# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-21 00:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reimbursement', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicaldetail',
            name='specialist_consultant_designation',
            field=models.CharField(blank=True, help_text=b'Designation of the Specialist', max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='medicaldetail',
            name='specialist_consultant_hospital',
            field=models.CharField(blank=True, help_text=b'Name of the hospital or dispensary', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='medicaldetail',
            name='specialist_consultant_name',
            field=models.CharField(blank=True, help_text=b'Full name of the Specialist', max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='medicaldetail',
            name='specialist_consultation_place',
            field=models.CharField(blank=True, help_text=b'Mention where consultation with the specialist took place', max_length=150, null=True),
        ),
    ]