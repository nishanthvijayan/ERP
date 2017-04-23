from django.shortcuts import render

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from reimbursement.models.medical import Medical
from reimbursement.models.medical.state import STATE


def reimbursement_submissions(request):
    medical_list = Medical.objects.all()
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
    return render(request, 'reimbursement/submissions.html', context)
