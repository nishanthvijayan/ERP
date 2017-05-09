from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404
from django.forms import modelformset_factory
from django.db import transaction, IntegrityError

from erp_core.models import Employee

from reimbursement.models.medical.medical import Medical
from reimbursement.models.medical.medical_detail.consultation import Consultation
from reimbursement.models.medical.medical_detail.injection import Injection
from reimbursement.models.medical.medical_detail.specialist_consultation import SpecialistConsultation
from reimbursement.models.medical.medical_detail.medicine import Medicine
from reimbursement.models.medical.medical_detail.medical_bill import MedicalBill

from reimbursement.forms.medical.general_detail.general_detail import GeneralDetailForm
from reimbursement.forms.medical.medical_detail.medical_detail import MedicalDetailForm
from reimbursement.forms.medical.medical_detail.medical_bill import MedicalBillForm
from reimbursement.forms.medical.amount_detail.amount_detail import AmountDetailFormForEmployee
from reimbursement.forms.medical.medical_detail.consultation import ConsultationForm
from reimbursement.forms.medical.medical_detail.specialist_consultation import SpecialistConsultationForm
from reimbursement.forms.medical.medical_detail.injection import InjectionForm
from reimbursement.forms.medical.medical_detail.medicine import MedicineForm


def new(request):
    if request.user.groups.filter(name='Employee').exists():

        ConsultationFormSet = modelformset_factory(
            Consultation,
            form=ConsultationForm,
            fields=('date', 'fee')
        )
        InjectionFormSet = modelformset_factory(
            Injection,
            form=InjectionForm,
            fields=('date', 'fee')
        )
        SpecialistConsultationFormSet = modelformset_factory(
            SpecialistConsultation,
            form=SpecialistConsultationForm,
            fields=('date', 'fee')
        )
        MedicineFormSet = modelformset_factory(
            Medicine,
            form=MedicineForm,
            fields=('name', 'price')
        )
        MedicalBillFormSet = modelformset_factory(
            MedicalBill,
            form=MedicalBillForm,
            fields=('image_file',)
        )

        if request.method == 'POST':

            if not request.POST.get('SUBMITTED', False):
                return redirect('reimbursement:reimbursement-index')

            general_detail_form = GeneralDetailForm(data=request.POST, prefix="general_detail_form")
            medical_detail_form = MedicalDetailForm(data=request.POST, files=request.FILES, prefix="medical_detail_form")
            amount_detail_form = AmountDetailFormForEmployee(data=request.POST, prefix="amount_detail_form")
            consultation_formset = ConsultationFormSet(
                data=request.POST,
                prefix="consultation_formset",
                queryset=Consultation.objects.none()
            )
            injection_formset = InjectionFormSet(
                data=request.POST,
                prefix="injection_formset",
                queryset=Injection.objects.none()
            )
            specialist_consultation_formset = SpecialistConsultationFormSet(
                data=request.POST,
                prefix="specialist_consultation_formset",
                queryset=SpecialistConsultation.objects.none()
            )
            medicine_formset = MedicineFormSet(
                data=request.POST,
                prefix="medicine_formset",
                queryset=Medicine.objects.none()
            )
            medical_bill_formset = MedicalBillFormSet(
                data=request.POST,
                files=request.FILES,
                prefix="medical_bill_formset",
                queryset=Medicine.objects.none()
            )

            if general_detail_form.is_valid() \
                    and medical_detail_form.is_valid() \
                    and amount_detail_form.is_valid() \
                    and consultation_formset.is_valid() \
                    and injection_formset.is_valid() \
                    and specialist_consultation_formset.is_valid() \
                    and medical_bill_formset.is_valid() \
                    and medicine_formset.is_valid():
                try:
                    with transaction.atomic():

                        general_detail_form_obj = general_detail_form.save(commit=False)
                        general_detail_form_obj.employee = Employee.objects.filter(user=request.user).first()
                        general_detail_form_obj.save()

                        medical = Medical.objects.create(general_detail=general_detail_form_obj)

                        medical_detail_form_obj = medical_detail_form.save(commit=False)
                        medical_detail_form_obj.medical = medical
                        medical_detail_form_obj.save()

                        net_amount_claimed = 0

                        amount_detail_form_obj = amount_detail_form.save(commit=False)
                        amount_detail_form_obj.medical = medical
                        amount_detail_form_obj.save()

                        medical_detail = medical.medical_detail

                        for consultation_form in consultation_formset:
                            if consultation_form.has_changed():
                                consultation_form_obj = consultation_form.save(commit=False)
                                consultation_form_obj.medical_detail = medical_detail
                                consultation_form_obj.save()
                                amount_detail_form_obj.amount_claimed_other += consultation_form_obj.fee

                        for injection_form in injection_formset:
                            if injection_form.has_changed():
                                injection_form_obj = injection_form.save(commit=False)
                                injection_form_obj.medical_detail = medical_detail
                                injection_form_obj.save()
                                amount_detail_form_obj.amount_claimed_other += injection_form_obj.fee

                        for specialist_consultation_form in specialist_consultation_formset:
                            if specialist_consultation_form.has_changed():
                                specialist_consultation_form_obj = specialist_consultation_form.save(commit=False)
                                specialist_consultation_form_obj.medical_detail = medical_detail
                                specialist_consultation_form_obj.save()
                                amount_detail_form_obj.amount_claimed_other += specialist_consultation_form_obj.fee

                        for medical_bill_form in medical_bill_formset:
                            if medical_bill_form.has_changed():
                                medical_bill_form_obj = medical_bill_form.save(commit=False)
                                medical_bill_form_obj.medical_detail = medical_detail
                                medical_bill_form_obj.save()

                        medicine_cost = 0

                        for medicine_form in medicine_formset:
                            if medicine_form.has_changed():
                                medicine_form_obj = medicine_form.save(commit=False)
                                medicine_form_obj.medical_detail = medical_detail
                                medicine_form_obj.save()
                                medicine_cost += medicine_form_obj.price

                        amount_detail_form_obj.amount_claimed_medicine = medicine_cost
                        amount_detail_form_obj.save()

                        net_amount_claimed += (amount_detail_form_obj.amount_claimed_other
                                               + amount_detail_form_obj.amount_claimed_medicine)

                        if amount_detail_form_obj.amount_claimed_test:
                            net_amount_claimed += amount_detail_form_obj.amount_claimed_test

                        if not amount_detail_form_obj.amount_claimed_room_rent:
                            net_amount_claimed += amount_detail_form_obj.amount_claimed_room_rent

                        messages.success(request, 'New reimbursement request submitted successfully with ID #'
                                         + str(medical.id))
                        return redirect('reimbursement:medical-show', medical.id)

                except IntegrityError:  # If the transaction failed
                    messages.error(request, 'There was an error submitting your reimbursement request.')
        else:
            general_detail_form = GeneralDetailForm(prefix="general_detail_form")
            medical_detail_form = MedicalDetailForm(prefix="medical_detail_form")
            amount_detail_form = AmountDetailFormForEmployee(prefix="amount_detail_form")
            consultation_formset = ConsultationFormSet(
                prefix="consultation_formset",
                queryset=Consultation.objects.none()
            )
            injection_formset = InjectionFormSet(
                prefix="injection_formset",
                queryset=Injection.objects.none()
            )
            specialist_consultation_formset = SpecialistConsultationFormSet(
                prefix="specialist_consultation_formset",
                queryset=SpecialistConsultation.objects.none()
            )
            medicine_formset = MedicineFormSet(
                prefix="medicine_formset",
                queryset=Medicine.objects.none()
            )
            medical_bill_formset = MedicalBillFormSet(
                prefix="medical_bill_formset",
                queryset=Medicine.objects.none()
            )

        context = {
            'general_detail_form': general_detail_form,
            'medical_detail_form': medical_detail_form,
            'amount_detail_form': amount_detail_form,
            'consultation_formset': consultation_formset,
            'injection_formset': injection_formset,
            'specialist_consultation_formset': specialist_consultation_formset,
            'medicine_formset': medicine_formset,
            'medical_bill_formset': medical_bill_formset
        }
        return render(request, 'reimbursement/medical/new.html', context)
    else:
        raise Http404
