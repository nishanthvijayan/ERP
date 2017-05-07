# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-05-07 08:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0006_transitionhistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseindentrequest',
            name='proprietary_distributor',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='purchaseindentrequest',
            name='proprietary_owner',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='purchaseindentrequest',
            name='make_or_model_reason',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]