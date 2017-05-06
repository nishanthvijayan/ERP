# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-05 17:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django_fsm


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('erp_core', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='MpHall',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('date', models.DateField(help_text=b'Enter the date of booking')),
                ('from_time', models.TimeField(help_text=b'Enter the booking start time')),
                ('to_time', models.TimeField(help_text=b'Enter the booking end time')),
                ('purpose', models.CharField(help_text=b'Enter the purpose of booking', max_length=100)),
                ('laptop_req', models.IntegerField(help_text=b'Enter the number of laptops required')),
                ('projector_req', models.IntegerField(help_text=b'Enter the number of projectors required')),
                ('audio_req', models.IntegerField(help_text=b'Enter the number of audio systems required')),
                ('video_req', models.IntegerField(help_text=b'Enter the number of video conferencing systems required')),
                ('state', django_fsm.FSMField(blank=True, default=b'Submitted', max_length=50)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mp_hall_booking', to='erp_core.Employee')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
