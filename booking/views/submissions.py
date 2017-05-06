from django.shortcuts import render

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from booking.models.mp_hall.mp_hall import MpHall

def booking_submissions(request):
    mp_hall_list = MpHall.objects.filter(employee__user_id=request.user.id)
    page = request.GET.get('page')
    paginator = Paginator(mp_hall_list, 10)
    try:
        mp_halls = paginator.page(page)
    except PageNotAnInteger:
        mp_halls = paginator.page(1)
    except EmptyPage:
        mp_halls = paginator.page(paginator.num_pages)
    context = {
        'mp_halls': mp_halls
    }
    return render(request, 'booking/submissions.html', context)