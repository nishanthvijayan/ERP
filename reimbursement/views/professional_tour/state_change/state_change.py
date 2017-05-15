from django.http import Http404
from django.shortcuts import render


from reimbursement.models.professional_tour.professional_tour import ProfessionalTour

from reimbursement.models.professional_tour.state import STATE

from reimbursement.views.professional_tour.state_change.role_based.head_of_department import generate_state_change_head_of_department

from reimbursement.views.professional_tour.state_change.role_based.dealing_assistant import generate_state_change_dealing_assistant

from reimbursement.views.professional_tour.state_change.role_based.senior_audit_officer import generate_state_change_senior_audit_officer

from reimbursement.views.professional_tour.state_change.role_based.assistant_registrar import generate_state_change_assistant_registrar


from reimbursement.views.professional_tour.state_change.role_based.registrar import generate_state_change_registrar


from reimbursement.views.professional_tour.state_change.role_based.registrar import generate_state_change_registrar


def state_change(request, professional_tour_id):

    if ProfessionalTour.objects.filter(id=professional_tour_id).exists():
        employee = request.user.employee_set.all().first()
        if employee:
            if employee.department.hod.user.id == employee.user.id:
                if ProfessionalTour.objects.filter(id=professional_tour_id).filter(state=STATE.SUBMITTED).exists():
                    return generate_state_change_head_of_department(request, professional_tour_id)
                if request.user.groups.filter(name='DA_AccountsDepartment').exists() \
                        and ProfessionalTour.objects.filter(id=professional_tour_id).filter(state=STATE.APPROVED_BY_HOD).exists():
                    return generate_state_change_dealing_assistant(request, professional_tour_id)
                if request.user.groups.filter(name='SrAO_AuditDepartment').exists() \
                        and ProfessionalTour.objects.filter(id=professional_tour_id).filter(state=STATE.APPROVED_BY_DA).exists():
                    return generate_state_change_senior_audit_officer(request, professional_tour_id)
                if request.user.groups.filter(name='AR_AdministrativeDepartment').exists() \
                        and ProfessionalTour.objects.filter(id=professional_tour_id).filter(state=STATE.APPROVED_BY_SrAO).exists():
                    return generate_state_change_assistant_registrar(request, professional_tour_id)
                if request.user.groups.filter(name='R_AdministrativeDepartment').exists() \
                        and ProfessionalTour.objects.filter(id=professional_tour_id).filter(state=STATE.APPROVED_BY_AR).exists():
                    return generate_state_change_registrar(request, professional_tour_id)
                else:
                    raise Http404
    else:
        raise Http404
