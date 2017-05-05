from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404
from django.forms import formset_factory
from django.db import transaction, IntegrityError

from erp_core.models import Employee

from reimbursement.models.medical.medical import Medical

from reimbursement.forms.medical.general_detail.general_detail import GeneralDetailForm
from reimbursement.forms.medical.medical_detail.medical_detail import MedicalDetailForm
from reimbursement.forms.medical.medical_detail.consultation import ConsultationForm
from reimbursement.forms.medical.medical_detail.specialist_consultation import SpecialistConsultationForm
from reimbursement.forms.medical.medical_detail.injection import InjectionForm


def new(request):
    if request.user.groups.filter(name='Employee').exists():

        ConsultationFormSet = formset_factory(ConsultationForm)
        SpecialistConsultationFormSet = formset_factory(SpecialistConsultationForm)
        InjectionFormSet = formset_factory(InjectionForm)

        if request.method == 'POST':

            general_detail_form = GeneralDetailForm(data=request.POST, prefix="general_detail_form")
            medical_detail_form = MedicalDetailForm(data=request.POST, prefix="medical_detail_form")
            consultation_formset = ConsultationFormSet(data=request.POST, prefix="consultation_formset")
            specialist_consultation_formset = SpecialistConsultationFormSet(data=request.POST,
                                                                            prefix="specialist_consultation_formset")
            injection_formset = InjectionForm(data=request.POST, prefix="injection_formset")

            if general_detail_form.is_valid() \
                    and medical_detail_form.is_valid() \
                    and consultation_formset.is_valid() \
                    and specialist_consultation_formset.is_valid():
                try:
                    with transaction.atomic():

                        general_detail_form_obj = general_detail_form.save(commit=False)
                        general_detail_form_obj.employee = Employee.objects.filter(user=request.user).first()
                        general_detail_form_obj = general_detail_form.save()

                        medical = Medical.objects.create(general_detail=general_detail_form_obj)

                        medical_detail_form_obj = medical_detail_form.save(commit=False)
                        medical_detail_form_obj.medical = medical
                        medical_detail_form_obj = medical_detail_form.save()

                        for consultation_form in consultation_formset:
                            consultation_form_obj = consultation_form.save(commit=False)
                            consultation_form_obj.medical = medical_detail_form_obj
                            consultation_form.save()

                        for injection_form in injection_formset:
                            injection_form_obj = injection_form.save(commit=False)
                            injection_form_obj.medical = medical_detail_form_obj
                            injection_form_obj.save()

                        for specialist_consultation_form in specialist_consultation_formset:
                            specialist_consultation_form_obj = specialist_consultation_form.save(commit=False)
                            specialist_consultation_form_obj.medical = medical_detail_form_obj
                            specialist_consultation_form_obj.save()

                        messages.success(request, 'New reimbursement request submitted successfully with ID #'
                                         + str(medical.id))
                        return redirect('reimbursement:medical-new')

                except IntegrityError:  # If the transaction failed
                    messages.error(request, 'There was an error submitting your reimbursement request.')
        else:
            general_detail_form = GeneralDetailForm(prefix="general_detail_form")
            medical_detail_form = MedicalDetailForm(prefix="medical_detail_form")
            consultation_formset = ConsultationFormSet(prefix="consultation_formset")
            specialist_consultation_formset = SpecialistConsultationFormSet(prefix="specialist_consultation_formset")
            injection_formset = InjectionFormSet(prefix="injection_formset")

        context = {
            'general_detail_form': general_detail_form,
            'medical_detail_form': medical_detail_form,
            'consultation_formset': consultation_formset,
            'specialist_consultation_formset': specialist_consultation_formset,
            'injection_formset': injection_formset
        }
        return render(request, 'reimbursement/medical/new.html', context)
    else:
        raise Http404
