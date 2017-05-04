from django.shortcuts import render
from django.http import Http404

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from reimbursement.models.medical import Medical
from reimbursement.models.medical.state import STATE


def reimbursement_requests_pending(request):
    if request.user.groups.filter(name='Reimbursement_Medical_Change_State').exists():
        medical_list = get_medical_list(request)
        page = request.GET.get('page')
        paginator = Paginator(medical_list, 10)
        try:
            medicals = paginator.page(page)
        except PageNotAnInteger:
            medicals = paginator.page(1)
        except EmptyPage:
            medicals = paginator.page(paginator.num_pages)
        context = {
            'medicals': medicals
        }
        return render(request, 'reimbursement/requests_pending.html', context)
    else:
        raise Http404


def get_medical_list(request):
    if request.user.groups.filter(name='AAO_AccountsDepartment').exists():
        medical_list = Medical.objects.filter(state=STATE.SUBMITTED)
    elif request.user.groups.filter(name='MS_HealthCareDepartment').exists():
        medical_list = Medical.objects.filter(state=STATE.VERIFIED_BY_DA    )
    elif request.user.groups.filter(name='DR_AccountsDepartment').exists():
        medical_list = Medical.objects.filter(state=STATE.APPROVED_BY_MS)
    elif request.user.groups.filter(name='SrAO_AuditDepartment').exists():
        medical_list = Medical.objects.filter(state=STATE.APPROVED_BY_DR)
    elif request.user.groups.filter(name='R_AdministrativeDepartment').exists():
        medical_list = Medical.objects.filter(state=STATE.APPROVED_BY_SrAO)
    elif request.user.groups.filter(name='JrAO_AccountsDepartment').exists():
        medical_list = Medical.objects.filter(state=STATE.APPROVED_BY_R)
    else:
        medical_list = Medical.objects.none()
    return medical_list
