from django.shortcuts import render
from django.http import Http404


def booking_index(request):
    # if request.user.groups.filter(name='Employee').exists():
    return render(request, 'booking/index.html')
    # else:
    #     raise Http404
