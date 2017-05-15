# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-08 18:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django_fsm


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('erp_core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('specification', models.TextField(max_length=500)),
                ('quantity', models.IntegerField()),
                ('estimated_cost', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('type', models.CharField(choices=[(b'lab_consumables', b'Lab Consumables'), (b'general_items', b'General Items'), (b'lab_equipments', b'Lab Equipment(s)'), (b'office_equipments', b'Office Equipment(s)'), (b'lab_furniture', b'Lab Furniture'), (b'office_furniture', b'Office Furniture')], max_length=30)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PurchaseIndentRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('project_name', models.CharField(max_length=200)),
                ('budget_head', models.CharField(max_length=50)),
                ('make_or_model_reason', models.TextField(blank=True, max_length=500, null=True)),
                ('proprietary_owner', models.CharField(blank=True, max_length=100, null=True)),
                ('proprietary_distributor', models.CharField(blank=True, max_length=100, null=True)),
                ('state', django_fsm.FSMField(blank=True, default=b'Submitted', max_length=50)),
                ('budgetary_approval', models.ImageField(blank=True, upload_to=b'budgetary_approval')),
                ('directors_approval', models.ImageField(blank=True, upload_to=b'directors_approval')),
                ('project_approval', models.ImageField(blank=True, upload_to=b'project_approval')),
                ('budget_sanctioned', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('amount_already_spent', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('budget_available', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('indenter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp_core.Employee')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TransitionHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('from_state', models.CharField(max_length=50)),
                ('to_state', models.CharField(max_length=50)),
                ('remark', models.TextField(max_length=500)),
                ('approver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp_core.Employee')),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchase.PurchaseIndentRequest')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200)),
                ('address', models.TextField(max_length=500)),
                ('email', models.EmailField(max_length=50)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchase.Item')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='item',
            name='purchase_request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchase.PurchaseIndentRequest'),
        ),
    ]
