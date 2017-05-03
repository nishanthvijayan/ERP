from django.shortcuts import render
from django.http import Http404

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from reimbursement.models.medical import Medical
from reimbursement.models.medical.state import STATE


def generate_state_change_dealing_assistant(request, medical_id):
    return render(request, 'reimbursement/medical/state_change/role_based/dealing_assistant.html')
