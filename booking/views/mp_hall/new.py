from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404
from django.forms import modelformset_factory
from django.db import transaction, IntegrityError

from erp_core.models import Employee

from booking.models.mp_hall.mp_hall import MpHall

from booking.forms.mp_hall.mp_hall import MpHallForm


def new(request):
    if request.user.groups.filter(name='Employee').exists():

        if request.method == 'POST':

            if not request.POST['SUBMITTED']:
                return redirect('booking:booking-index')

            mp_hall_form = MpHallForm(data=request.POST, prefix="booking-form")

            if mp_hall_form.is_valid():
                try:
                    with transaction.atomic():

                        mp_hall_form_obj = mp_hall_form.save(commit=False)
                        mp_hall_form_obj.employee = Employee.objects.filter(user=request.user).first()
                        mp_hall_form_obj.save()

                        messages.success(request, 'New MP Hall booking request submitted successfully with ID #'
                                         + str(mp_hall_form_obj.id))
                        return redirect('booking:mp-hall-show', mp_hall_form_obj.id)

                except IntegrityError:  # If the transaction failed
                    messages.error(request, 'There was an error submitting your booking request.')
        else:
            mp_hall_form = MpHallForm(prefix="booking-form")

        context = {
            'mp_hall_form': mp_hall_form
        }
        return render(request, 'booking/mp_hall/new.html', context)
    else:
        raise Http404
