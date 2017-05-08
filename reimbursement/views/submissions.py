from django.shortcuts import render

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from itertools import chain
from operator import attrgetter

from reimbursement.models.medical import Medical
from reimbursement.models.telephone_expense.telephone_expense import TelephoneExpense


def reimbursement_submissions(request):
    medical_list = Medical.objects.filter(general_detail__employee__user_id=request.user.id)
    telephone_expense_list = TelephoneExpense.objects.filter(employee__user_id=request.user.id)

    result_list = sorted(
        chain(medical_list, telephone_expense_list),
        key=attrgetter('modified_at'),
        reverse=True
    )

    print result_list

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
    return render(request, 'reimbursement/submissions.html', context)
