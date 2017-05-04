from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import Http404

from reimbursement.models.medical import Medical

from reimbursement.forms.medical.amount_detail.amount_detail import AmountDetailForm


def generate_state_change_dealing_assistant(request, medical_id):
    medical = get_object_or_404(Medical, id=medical_id)
    if request.method == 'POST':
        form = AmountDetailForm(data=request.POST)
        if form.is_valid():
            if form.save():
                messages.success(request, 'Response for medical reimbursement #<ID> \'' + '\' successfully registered!')
            else:
                messages.error(request, 'Some error occurred')
            return redirect('reimbursement:medical-show',2)
    else:
        form = AmountDetailForm()
    context = {
        "medical": medical,
        "form" : form
    }
    return render(request, 'reimbursement/medical/state_change/role_based/dealing_assistant.html', context)
