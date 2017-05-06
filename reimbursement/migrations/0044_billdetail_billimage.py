# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-06 17:31
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import reimbursement.models.telephone_expense.bill.bill_image


class Migration(migrations.Migration):

    dependencies = [
        ('reimbursement', '0043_telephoneexpenses'),
    ]

    operations = [
        migrations.CreateModel(
            name='BillDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('bill_number', models.CharField(help_text=b'Enter bill number mentioned on the bill', max_length=10)),
                ('bill_date', models.DateField(help_text=b'Enter date mentioned on the bill')),
                ('date_form', models.DateField(help_text=b'Enter starting date of the billing')),
                ('date_to', models.DateField(help_text=b'Enter finishing date of the billing')),
                ('phone_number', models.CharField(help_text=b'Enter phone number', max_length=12, validators=[django.core.validators.RegexValidator(message=b'Phone number must be entered in the format', regex=b'^\\+?1?\\d{9,12}$')])),
                ('is_telephone_line', models.BooleanField(help_text=b'Is it a telephone number')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BillImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('image_file', models.ImageField(help_text=b'Upload Image of bills', upload_to=reimbursement.models.telephone_expense.bill.bill_image.generate_filename)),
                ('telephone_expense', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bill_image', to='reimbursement.TelephoneExpenses')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
