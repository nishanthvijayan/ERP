from django.http import Http404

from reimbursement.models.medical import Medical

from reimbursement.models.medical.state import STATE

from role_based.dealing_assistant import generate_state_change_dealing_assistant
from role_based.medical_superintendent import generate_state_change_medical_superintendent
from role_based.deputy_registrar import generate_state_change_deputy_registrar
from role_based.senior_audit_officer import generate_state_change_senior_audit_officer
from role_based.registrar import generate_state_change_registrar
from role_based.junior_accounting_officer import generate_state_change_junior_accounting_officer


def state_change(request, medical_id):
    if Medical.objects.filter(id=medical_id).exists():
        if request.user.groups.filter(name='AAO_AccountsDepartment').exists() \
                and Medical.objects.filter(id=medical_id).filter(state=STATE.SUBMITTED).exists():
            return generate_state_change_dealing_assistant(request, medical_id)
        elif request.user.groups.filter(name='MS_HealthCareDepartment').exists() \
                and Medical.objects.filter(id=medical_id).filter(state=STATE.VERIFIED_BY_DA).exists():
            return generate_state_change_medical_superintendent(request, medical_id)
        elif request.user.groups.filter(name='DR_AccountsDepartment').exists() \
                and Medical.objects.filter(id=medical_id).filter(state=STATE.APPROVED_BY_MS).exists():
            return generate_state_change_deputy_registrar(request, medical_id)
        elif request.user.groups.filter(name='SrAO_AuditDepartment').exists() \
                and Medical.objects.filter(id=medical_id).filter(state=STATE.APPROVED_BY_DR).exists():
            return generate_state_change_senior_audit_officer(request, medical_id)
        elif request.user.groups.filter(name='R_AdministrativeDepartment').exists() \
                and Medical.objects.filter(id=medical_id).filter(state=STATE.APPROVED_BY_SrAO).exists():
            return generate_state_change_registrar(request, medical_id)
        elif request.user.groups.filter(name='JrAO_AccountsDepartment').exists() \
                and Medical.objects.filter(id=medical_id).filter(state=STATE.APPROVED_BY_R).exists():
            return generate_state_change_junior_accounting_officer(request, medical_id)
        else:
            raise Http404
    else:
        raise Http404
