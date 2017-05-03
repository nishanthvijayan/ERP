from django.shortcuts import render
from django.http import Http404


def state_change(request, medical_id):
    if request.user.groups.filter(name='Reimbursement_Medical_Change_State').exists():
        if request.user.groups.filter(name='AAO_AccountsDepartment').exists():
            pass
        elif request.user.groups.filter(name='MS_HealthCareDepartment').exists():
            pass
        elif request.user.groups.filter(name='DR_AccountsDepartment').exists():
            pass
        elif request.user.groups.filter(name='SrAO_AuditDepartment').exists():
            pass
        elif request.user.groups.filter(name='R_AdministrativeDepartment').exists():
            pass
        elif request.user.groups.filter(name='JrAO_AccountsDepartment').exists():
            pass
        else:
            raise Http404
    else:
        raise Http404
