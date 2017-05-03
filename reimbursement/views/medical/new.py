from django.shortcuts import render
from django.http import Http404

from reimbursement.models.medical.medical import Medical


def new(request):
    if request.user.groups.filter(name='Employee').exists():
        return render(request, 'reimbursement/medical/new.html')
    else:
        raise Http404
