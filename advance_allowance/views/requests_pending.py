from django.shortcuts import render
from django.http import Http404

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from advance_allowance.models.travel_allowance_advance.travel_allowance_advance import TravelAllowanceAdvance
from advance_allowance.models.travel_allowance_advance.travel_allowance_advance import STATE


def advance_allowance_requests_pending(request):
    if request.user.groups.filter(name='Advance_Allowance_Change_State').exists():
        advance_allowance_list = get_advance_allowance_list(request)
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
        return render(request, 'advance_allowance/requests_pending.html', context)
    else:
        raise Http404


def get_advance_allowance_list(request):
    if request.user.groups.filter(name='HOD').exists():
        advance_allowance_list = TravelAllowanceAdvance.objects.filter(state=STATE.SUBMITTED)
    elif request.user.groups.filter(name='JrA_AccountsDepartment').exists():
        advance_allowance_list = TravelAllowanceAdvance.objects.filter(state=STATE.APPROVED_BY_HOD)
    elif request.user.groups.filter(name='JAO_AuditDepartment').exists():
        advance_allowance_list = TravelAllowanceAdvance.objects.filter(state=STATE.APPROVED_BY_JRA)
    elif request.user.groups.filter(name='AR_AccountsDepartment').exists():
        advance_allowance_list = TravelAllowanceAdvance.objects.filter(state=STATE.APPROVED_BY_JAO)
    elif request.user.groups.filter(name='R_AdministrativeDepartment').exists():
        advance_allowance_list = TravelAllowanceAdvance.objects.filter(state=STATE.APPROVED_BY_ARA)
    elif request.user.groups.filter(name='JrAO_AccountsDepartment').exists():
        advance_allowance_list = TravelAllowanceAdvance.objects.filter(state=STATE.APPROVED_BY_R)
    else:
        advance_allowance_list = TravelAllowanceAdvance.objects.none()
    return advance_allowance_list
