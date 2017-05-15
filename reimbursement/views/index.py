from django.shortcuts import render
from django.http import Http404


def reimbursement_index(request):
    if request.user.groups.filter(name='Employee').exists():
        return render(request, 'reimbursement/index.html')
    else:
        raise Http404

