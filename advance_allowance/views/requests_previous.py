from django.shortcuts import render
from django.http import Http404


def advance_allowance_requests_previous(request):
    #if request.user.groups.filter(name='Employee').exists():
    return render(request, 'advance_allowance/requests_previous.html')
    # else:
    #     raise Http404