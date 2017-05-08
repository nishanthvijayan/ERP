from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404
from django.forms import modelformset_factory
from django.db import transaction, IntegrityError

from erp_core.models import Employee

from reimbursement.models.professional_tour.professional_tour import ProfessionalTour

from reimbursement.models.professional_tour.meeting_date.meeting_date import MeetingDate

from reimbursement.forms.professional_tour.professional_tour import ProfessionalTourFormForEmployee

from reimbursement.forms.professional_tour.meeting_date.meeting_date import MeetingDateFormForEmployee

from reimbursement.forms.professional_tour.professional_tour import ProfessionalTourFormForDA


def new(request):
    if request.user.groups.filter(name='Employee').exists():

        if request.method == 'POST':

            if not request.POST['SUBMITTED']:
                return redirect('reimbursement:reimbursement-index')

            professional_tour_form = ProfessionalTourFormForEmployee(data=request.POST, prefix="reimbursement-form")
            meeting_date_form = MeetingDateFormForEmployee(data=request.POST,prefix="reimbursement-form")

            if professional_tour_form.is_valid()\
                    and meeting_date_form.is_valid():
                try:
                    with transaction.atomic():

                        professional_tour_form_obj = professional_tour_form.save(commit=False)
                        professional_tour_form_obj.employee = Employee.objects.filter(user=request.user).first()
                        professional_tour_form_obj.save()

                        meeting_date_form_obj = meeting_date_form.save(commit=False)
                        meeting_date_form_obj.employee = Employee.objects.filter(user=request.user).first()
                        meeting_date_form_obj.save()

                        messages.success(request, 'New Reimbursement  request submitted successfully with ID #'
                                         + str(professional_tour_form_obj.id))
                        return redirect('reimbursement:professional-tour-show', professional_tour_form_obj.id)

                except IntegrityError:  # If the transaction failed
                    messages.error(request, 'There was an error submitting your reimbursement request.')
        else:
            professional_tour_form = ProfessionalTourFormForEmployee(prefix="reimbursement-form")
            meeting_date_form = MeetingDateFormForEmployee(prefix="reimbursement-form")

        context = {
            'professional_tour_form': professional_tour_form,
            'meeting_date_form': meeting_date_form,
        }
        return render(request, 'reimbursement/professional_tour/new.html', context)
    else:
        raise Http404