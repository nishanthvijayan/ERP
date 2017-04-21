# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-20 23:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import reimbursement.models.medical.medical_detail.medical_detail
import reimbursement.models.medical.medical_detail.medicine_bill


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('erp_core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AmountDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('amount_claimed_medicine', models.DecimalField(blank=True, decimal_places=2, help_text=b'The amount claimed for the medicines, if any', max_digits=12, null=True)),
                ('amount_claimed_test', models.DecimalField(blank=True, decimal_places=2, help_text=b'The amount claimed for the tests, if any', max_digits=12, null=True)),
                ('amount_claimed_room_rent', models.DecimalField(blank=True, decimal_places=2, help_text=b'The amount claimed for room rented, if any', max_digits=12, null=True)),
                ('amount_claimed_other', models.DecimalField(blank=True, decimal_places=2, help_text=b'Others, Ex :- Operation, Procedure, ICU / CCU/ Consultation / Others)', max_digits=12, null=True)),
                ('other_expenses', models.CharField(blank=True, help_text=b'Please specify, Ex :- Operation, Procedure, ICU / CCU/ Consultation / Others)', max_length=150, null=True)),
                ('amount_passed_medicine', models.DecimalField(blank=True, decimal_places=2, help_text=b'The amount passed for the medicines, if any', max_digits=12, null=True)),
                ('amount_passed_test', models.DecimalField(blank=True, decimal_places=2, help_text=b'The amount passed for the tests, if any', max_digits=12, null=True)),
                ('amount_passed_room_rent', models.DecimalField(blank=True, decimal_places=2, help_text=b'The amount passed for room rented, if any', max_digits=12, null=True)),
                ('amount_passed_other', models.DecimalField(blank=True, decimal_places=2, help_text=b'Others, Ex :- Operation, Procedure, ICU / CCU/ Consultation / Others)', max_digits=12, null=True)),
                ('total_amount_claimed', models.DecimalField(blank=True, decimal_places=2, help_text=b'Total amount claimed', max_digits=12)),
                ('total_amount_passed', models.DecimalField(blank=True, decimal_places=2, help_text=b'Total amount passed', max_digits=12)),
                ('total_amount_rejected', models.DecimalField(blank=True, decimal_places=2, help_text=b'Total amount rejected', max_digits=12)),
                ('medical_reimbursement_register_page_no', models.PositiveIntegerField(help_text=b'Medical reimbursement register page number')),
                ('medical_reimbursement_register_sr_no', models.PositiveIntegerField(help_text=b'Medical reimbursement register serial number', unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Consultation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('date', models.DateField(help_text=b'Consultation Date')),
                ('fee', models.PositiveIntegerField(help_text=b'Consultation Fee')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GeneralDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('patient_name', models.CharField(help_text=b'Full name of the patient', max_length=150)),
                ('patient_age', models.PositiveSmallIntegerField(help_text=b'Age of the patient')),
                ('employee_relationship', models.CharField(help_text=b'Relationship with the employee', max_length=150)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp_core.Employee')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Injection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('date', models.DateField(help_text=b'Injection Date')),
                ('fee', models.PositiveIntegerField(help_text=b'Injection Fee')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Medical',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('general_detail', models.ForeignKey(help_text=b'General details ID of the GeneralDetail', on_delete=django.db.models.deletion.CASCADE, to='reimbursement.GeneralDetail')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MedicalDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('place_at_which_patient_fell_ill', models.CharField(help_text=b'Mention the place where the patient fell ill', max_length=150)),
                ('consultant_name', models.CharField(help_text=b'Full name of the medical officer', max_length=150)),
                ('consultant_designation', models.CharField(help_text=b'Designation of the medical officer', max_length=150)),
                ('consultant_hospital', models.CharField(help_text=b'Name of the hospital or dispensary', max_length=200)),
                ('consultation_place', models.CharField(help_text=b'Mention where consultation took place, for multiple places use commas', max_length=150)),
                ('injection_place', models.CharField(help_text=b'Mention the place where injection held, for multiple places use commas', max_length=150)),
                ('diagnosis_place', models.CharField(help_text=b'Mention the hospital or laboratory where diagnosis held', max_length=150)),
                ('diagnosis_advised', models.BooleanField(help_text=b'Whether the tests were under taken on the advice of the authorized medical attendant. If so certificate to the effect should be attached.')),
                ('diagnosis_advised_certificate', models.ImageField(blank=True, help_text=b'Upload Image of the certificate', null=True, upload_to=reimbursement.models.medical.medical_detail.medical_detail.diagnosis_advised_certificate_filename)),
                ('cost_of_medicines_market', models.PositiveIntegerField(blank=True, help_text=b'Mention cost of medicines purchased from market', null=True)),
                ('specialist_consultant_name', models.CharField(help_text=b'Full name of the Specialist', max_length=150)),
                ('specialist_consultant_designation', models.CharField(help_text=b'Designation of the Specialist', max_length=150)),
                ('specialist_consultant_hospital', models.CharField(help_text=b'Name of the hospital or dispensary', max_length=200)),
                ('specialist_consultation_place', models.CharField(help_text=b'Mention where consultation with the specialist took place', max_length=150)),
                ('total_amount_claimed', models.DecimalField(decimal_places=2, help_text=b'Total claim amount', max_digits=12)),
                ('less_amount_taken', models.DecimalField(decimal_places=2, help_text=b'Less advance taken', max_digits=12)),
                ('net_amount_taken', models.DecimalField(decimal_places=2, help_text=b'Net amount', max_digits=12)),
                ('medical', models.OneToOneField(help_text=b'Refers to Medical Model', on_delete=django.db.models.deletion.CASCADE, to='reimbursement.Medical')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(help_text=b'Name of the medicine', max_length=200)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('medical_detail', models.ForeignKey(help_text=b'Model detail id', on_delete=django.db.models.deletion.CASCADE, to='reimbursement.MedicalDetail')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MedicineBill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('image_file', models.ImageField(help_text=b'Upload Image of bills', upload_to=reimbursement.models.medical.medical_detail.medicine_bill.generate_filename)),
                ('medical_detail', models.ForeignKey(help_text=b'Medical detail id', on_delete=django.db.models.deletion.CASCADE, to='reimbursement.MedicalDetail')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SpecialistConsultation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('date', models.DateField(help_text=b'Specialist Consultation Date')),
                ('fee', models.PositiveIntegerField(help_text=b'Specialist Consultation Fee')),
                ('medical_detail', models.ForeignKey(help_text=b'Medical detail id', on_delete=django.db.models.deletion.CASCADE, to='reimbursement.MedicalDetail')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='injection',
            name='medical_detail',
            field=models.ForeignKey(help_text=b'Medical detail id', on_delete=django.db.models.deletion.CASCADE, to='reimbursement.MedicalDetail'),
        ),
        migrations.AddField(
            model_name='consultation',
            name='medical_detail',
            field=models.ForeignKey(help_text=b'Medical detail id', on_delete=django.db.models.deletion.CASCADE, to='reimbursement.MedicalDetail'),
        ),
        migrations.AddField(
            model_name='amountdetail',
            name='medical',
            field=models.OneToOneField(help_text=b'Refers to Medical Model', on_delete=django.db.models.deletion.CASCADE, to='reimbursement.Medical'),
        ),
    ]