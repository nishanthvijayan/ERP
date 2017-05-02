from django.shortcuts import render
from django.http import Http404

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.models import Group

from reimbursement.models.medical import Medical


def reimbursement_requests_previous(request):
    if request.user.groups.filter(name='Reimbursement_Medical_Change_State').exists():
        if request.user.groups.filter(name='AAO_AccountsDepartment').exists():
            medical_list = Medical.objects.filter(
                transition_history_medical__approved_by_group=Group.objects.get(name="AAO_AccountsDepartment")
            )
        elif request.user.groups.filter(name='MS_HealthCareDepartment').exists():
            medical_list = Medical.objects.filter(
                transition_history_medical__approved_by_group=Group.objects.get(name="MS_HealthCareDepartment")
            )
        elif request.user.groups.filter(name='DR_AccountsDepartment').exists():
            medical_list = Medical.objects.filter(
                transition_history_medical__approved_by_group=Group.objects.get(name="DR_AccountsDepartment")
            )
        elif request.user.groups.filter(name='SrAO_AuditDepartment').exists():
            medical_list = Medical.objects.filter(
                transition_history_medical__approved_by_group=Group.objects.get(name="SrAO_AuditDepartment")
            )
        elif request.user.groups.filter(name='R_AdministrativeDepartment').exists():
            medical_list = Medical.objects.filter(
                transition_history_medical__approved_by_group=Group.objects.get(name="R_AdministrativeDepartment")
            )
        elif request.user.groups.filter(name='JrAO_AccountsDepartment').exists():
            medical_list = Medical.objects.filter(
                transition_history_medical__approved_by_group=Group.objects.get(name="JrAO_AccountsDepartment")
            )
        else:
            medical_list = Medical.objects.none()
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
        return render(request, 'reimbursement/requests_previous.html', context)
    else:
        raise Http404
