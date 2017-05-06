from django.shortcuts import render


def mp_hall_index(request):
    return render(request, 'booking/index.html')