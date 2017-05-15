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


def reimbursement_requests_previous(request):
    if request.user.groups.filter(
                    Q(
                        name='Reimbursement_Medical_Change_State'
                    ) |
                    Q(
                        name='Reimbursement_Telephone_Expense_Change_State'
                    )|
                    Q(
                        name='Reimbursement_Professional_Tour_Change_State'
                    )
    ).exists():
        if request.user.groups.filter(name='AAO_AccountsDepartment').exists():
            states = {
                'Medical': MEDICAL_STATE.SUBMITTED,
                'TelephoneExpense': TELEPHONE_EXPENSE_STATE.SUBMITTED
            }
        elif request.user.groups.filter(name='MS_HealthCareDepartment').exists():
            states = {
                'Medical': MEDICAL_STATE.APPROVED_BY_DA,
            }
        elif request.user.groups.filter(name='DR_AccountsDepartment').exists():
            states = {
                'Medical': MEDICAL_STATE.APPROVED_BY_MS,
                'TelephoneExpense': TELEPHONE_EXPENSE_STATE.APPROVED_BY_DA
            }
        elif request.user.groups.filter(name='SrAO_AuditDepartment').exists():
            states = {
                'Medical': MEDICAL_STATE.APPROVED_BY_DR,
                'TelephoneExpense': TELEPHONE_EXPENSE_STATE.APPROVED_BY_DR
            }
        elif request.user.groups.filter(name='R_AdministrativeDepartment').exists():
            states = {
                'Medical': MEDICAL_STATE.APPROVED_BY_SrAO,
                'TelephoneExpense': TELEPHONE_EXPENSE_STATE.APPROVED_BY_SrAO
            }
        elif request.user.groups.filter(name='JrA_AccountsDepartment').exists():
            states = {
                'Medical': MEDICAL_STATE.APPROVED_BY_R,
                'TelephoneExpense': TELEPHONE_EXPENSE_STATE.APPROVED_BY_R
            }
        else:
            states = {}
        result_list = get_reimbursement_list(request, states=states)
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
        return render(request, 'reimbursement/requests_previous.html', context)
    else:
        raise Http404


def get_reimbursement_list(request, states):
    """
    Generates List of all the reimbursement, ordered by recent date
    :param request: HTTPRequest Object
    :param states: State List for different type of reimbursement
    :return: list of all reimbursements
    """
    if states.get('Medical', False):
        medical_list = Medical.objects.filter(
            transition_history_medical__state_from=states['Medical']
        )
    else:
        medical_list = Medical.objects.none()

    if states.get('TelephoneExpense', False):
        telephone_expense_list = TelephoneExpense.objects.filter(
            transition_history_set__state_from=states['TelephoneExpense']
        )
        print telephone_expense_list
    else:
        telephone_expense_list = TelephoneExpense.objects.none()

    if states.get('ProfessionalTour', False):
        professional_tour_list = ProfessionalTour.objects.filter(
            professional_tour_transition_history__state_from=states['ProfessionalTour']
        )
    else:
        professional_tour_list = ProfessionalTour.objects.none()

    result_list = sorted(
        chain(medical_list, telephone_expense_list),
        key=attrgetter('modified_at'),
        reverse=True
    )

    return result_list
