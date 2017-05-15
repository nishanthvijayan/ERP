from django.shortcuts import render
from django.http import Http404
from django.db.models import Q

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from itertools import chain
from operator import attrgetter

from reimbursement.models.medical import Medical
from reimbursement.models.medical.state import STATE as MEDICAL_STATE

from reimbursement.models.telephone_expense.telephone_expense import TelephoneExpense
from reimbursement.models.telephone_expense.state import STATE as TELEPHONE_EXPENSE_STATE

from reimbursement.models.professional_tour.professional_tour import ProfessionalTour
from reimbursement.models.professional_tour.state import STATE as PROFESSIONAL_TOUR_STATE


def reimbursement_requests_pending(request):
    if request.user.groups.filter(
                    Q(
                        name='Reimbursement_Medical_Change_State'
                    ) |
                    Q(
                        name='Reimbursement_Telephone_Expense_Change_State'
                    ) |
                    Q(
                        name='Reimbursement_Professional_Tour_Change_State'
                    )
    ).exists():
        medical_list = get_medical_list(request)
        telephone_expense_list = get_telephone_expense_list(request)
        professional_tour_list = get_professional_tour_list(request)

        result_list = sorted(
            chain(medical_list, telephone_expense_list, professional_tour_list),
            key=attrgetter('modified_at'),
            reverse=True
        )

        page = request.GET.get('page')
        paginator = Paginator(result_list, 10)
        try:
            results = paginator.page(page)
        except PageNotAnInteger:
            results = paginator.page(1)
        except EmptyPage:
            results = paginator.page(paginator.num_pages)
        context = {
            'results': results
        }
        return render(request, 'reimbursement/requests_pending.html', context)
    else:
        raise Http404


def get_medical_list(request):
    if request.user.groups.filter(name='AAO_AccountsDepartment').exists():
        medical_list = Medical.objects.filter(state=MEDICAL_STATE.SUBMITTED)
    elif request.user.groups.filter(name='MS_HealthCareDepartment').exists():
        medical_list = Medical.objects.filter(state=MEDICAL_STATE.APPROVED_BY_DA)
    elif request.user.groups.filter(name='DR_AccountsDepartment').exists():
        medical_list = Medical.objects.filter(state=MEDICAL_STATE.APPROVED_BY_MS)
    elif request.user.groups.filter(name='SrAO_AuditDepartment').exists():
        medical_list = Medical.objects.filter(state=MEDICAL_STATE.APPROVED_BY_DR)
    elif request.user.groups.filter(name='R_AdministrativeDepartment').exists():
        medical_list = Medical.objects.filter(state=MEDICAL_STATE.APPROVED_BY_SrAO)
    elif request.user.groups.filter(name='JrAO_AccountsDepartment').exists():
        medical_list = Medical.objects.filter(state=MEDICAL_STATE.APPROVED_BY_R)
    else:
        medical_list = Medical.objects.none()
    return medical_list


def get_telephone_expense_list(request):
    if request.user.groups.filter(name='AAO_AccountsDepartment').exists():
        telephone_expense_list = TelephoneExpense.objects.filter(state=TELEPHONE_EXPENSE_STATE.SUBMITTED)
    elif request.user.groups.filter(name='DR_AccountsDepartment').exists():
        telephone_expense_list = TelephoneExpense.objects.filter(state=TELEPHONE_EXPENSE_STATE.APPROVED_BY_DA)
    elif request.user.groups.filter(name='SrAO_AuditDepartment').exists():
        telephone_expense_list = TelephoneExpense.objects.filter(state=TELEPHONE_EXPENSE_STATE.APPROVED_BY_DR)
    elif request.user.groups.filter(name='R_AdministrativeDepartment').exists():
        telephone_expense_list = TelephoneExpense.objects.filter(state=TELEPHONE_EXPENSE_STATE.APPROVED_BY_SrAO)
    elif request.user.groups.filter(name='JrAO_AccountsDepartment').exists():
        telephone_expense_list = TelephoneExpense.objects.filter(state=TELEPHONE_EXPENSE_STATE.APPROVED_BY_R)
    else:
        telephone_expense_list = TelephoneExpense.objects.none()
    return telephone_expense_list


def get_professional_tour_list(request):
    looged_in_employee = request.user.employee_set.all().first()
    if looged_in_employee:
        professional_tour_list = []
        if looged_in_employee.department.hod.user.id == looged_in_employee.user.id:
            professional_tour_list += ProfessionalTour.objects.filter(employee__department_id=looged_in_employee
                                                                      .department.id).filter(state=PROFESSIONAL_TOUR_STATE.SUBMITTED)
        elif request.user.groups.filter(name='DR_AccountsDepartment').exists():
            professional_tour_list += ProfessionalTour.objects.filter(state=PROFESSIONAL_TOUR_STATE.APPROVED_BY_HOD)
        elif request.user.groups.filter(name='SrAO_AuditDepartment').exists():
            professional_tour_list += ProfessionalTour.objects.filter(state=PROFESSIONAL_TOUR_STATE.APPROVED_BY_DR)
        elif request.user.groups.filter(name='AR_AdministrativeDepartment').exists():
            professional_tour_list += ProfessionalTour.objects.filter(state=PROFESSIONAL_TOUR_STATE.APPROVED_BY_SrAO)
        elif request.user.groups.filter(name='R_AdministrativeDepartment').exists():
            professional_tour_list += ProfessionalTour.objects.filter(state=PROFESSIONAL_TOUR_STATE.APPROVED_BY_AR)
        else:
            professional_tour_list = ProfessionalTour.objects.none()
        return professional_tour_list
