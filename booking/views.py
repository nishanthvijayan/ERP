from django.shortcuts import render


def booking_index(request):
    return render(request, 'booking/index.html')


def booking_submissions(request):
    return render(request, 'booking/submissions.html')


def booking_requests_pending(request):
    return render(request, 'booking/requests_pending.html')


def booking_requests_previous(request):
    return render(request, 'booking/requests_previous.html')