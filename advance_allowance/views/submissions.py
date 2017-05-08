from django.shortcuts import render

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from advance_allowance.models.travel_allowance_advance.travel_allowance_advance import TravelAllowanceAdvance


def advance_allowance_submissions(request):
    advance_allowance_list = TravelAllowanceAdvance.objects.filter(employee__user_id=request.user.id)
    print advance_allowance_list
    page = request.GET.get('page')
    paginator = Paginator(advance_allowance_list, 10)
    try:
        advance_allowances = paginator.page(page)
    except PageNotAnInteger:
        advance_allowances = paginator.page(1)
    except EmptyPage:
        advance_allowances = paginator.page(paginator.num_pages)
    context = {
        'advance_allowances': advance_allowances
    }
    return render(request, 'advance_allowance/submissions.html', context)