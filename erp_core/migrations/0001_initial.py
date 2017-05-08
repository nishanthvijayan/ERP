# Generated by Django 1.11 on 2017-05-05 21:41
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('address', models.CharField(max_length=150)),
                ('town_city', models.CharField(blank=True, help_text=b'This field is option as some places doesnt have town/city', max_length=50, null=True)),
                ('district', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('zipcode', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('short_name', models.CharField(help_text=b'Like CSE, EE, ME', max_length=20)),
                ('description', models.CharField(max_length=500)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('employee_id', models.IntegerField(help_text=b'UID for each employee')),
                ('nationality', models.CharField(max_length=50)),
                ('date_of_joining', models.DateField()),
                ('designation', models.CharField(max_length=100)),
                ('short_designation', models.CharField(max_length=100)),
                ('current_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='current_address', to='erp_core.Address')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp_core.Department')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Pay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('band', models.IntegerField(help_text=b'Band Pay')),
                ('grade', models.IntegerField(help_text=b'Grade Pay')),
                ('da', models.IntegerField(help_text=b'Dearness Allowance')),
                ('hra', models.IntegerField(help_text=b'House Rental Allowance')),
                ('ta', models.IntegerField(help_text=b'Travel Allowance')),
                ('gross', models.IntegerField(blank=True, help_text=b'Gross Total = Band + Grade + DA + HRA + TA')),
                ('nps', models.IntegerField(help_text=b'New Pension Scheme')),
                ('lic', models.IntegerField(help_text=b'LIC')),
                ('deduction', models.IntegerField(blank=True, help_text=b'Deductions = NPS + LIC')),
                ('net_salary', models.IntegerField(blank=True, help_text=b'Net Salary = Gross Total - Deductions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='employee',
            name='pay',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp_core.Pay'),
        ),
        migrations.AddField(
            model_name='employee',
            name='permanent_address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='permanent_address', to='erp_core.Address'),
        ),
        migrations.AddField(
            model_name='employee',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
