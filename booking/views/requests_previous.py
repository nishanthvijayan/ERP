from django.shortcuts import render


def booking_requests_previous(request):
    return render(request, 'booking/requests_previous.html')
