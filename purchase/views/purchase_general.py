from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

from erp_core.models import Department
from purchase.models import PurchaseIndentRequest, TransitionHistory


@login_required
def index(request):
    """View function that renders list of purchase list."""
    return render(request, 'purchase/index.html')


@login_required
def submissions(request):
    """View function that renders current users purchase related form submissions."""
    current_employee = request.user.employee_set.all()[0]
    submissions_list = PurchaseIndentRequest.objects.filter(indenter=current_employee)

    page = request.GET.get('page')
    paginator = Paginator(submissions_list, 10)
    try:
        submissions = paginator.page(page)
    except PageNotAnInteger:
        submissions = paginator.page(1)
    except EmptyPage:
        submissions = paginator.page(paginator.num_pages)

    return render(request, 'purchase/submissions.html', {'submissions': submissions})


@login_required
def requests_pending(request):
    """View function that renders list of purchase forms pending current user's approval."""
    current_employee = request.user.employee_set.all()[0]

    pending_requests_list_hod = PurchaseIndentRequest.objects.none()
    pending_requests_list_jao = PurchaseIndentRequest.objects.none()
    pending_requests_list_dr = PurchaseIndentRequest.objects.none()

    if Department.objects.filter(hod=current_employee).exists():
        subordinates = current_employee.department.employee_set.values_list('id', flat=True)
        pending_requests_list_hod = PurchaseIndentRequest.objects.filter(
            state='Submitted',
            indenter_id__in=subordinates
        )

    if request.user.groups.filter(name='JrAO_AccountsDepartment').exists():
        pending_requests_list_jao = PurchaseIndentRequest.objects.filter(state='Approved by Head of Department')

    if request.user.groups.filter(name='DR_AccountsDepartment').exists():
        pending_requests_list_dr = PurchaseIndentRequest.objects.filter(state='Approved by Junior Accounts Officer')

    # Merge different forms accssible via different possible roles, take distinct and sort

    pending_requests_list = (pending_requests_list_hod | pending_requests_list_jao |
                             pending_requests_list_dr).distinct().order_by('-created_at')

    page = request.GET.get('page')
    paginator = Paginator(pending_requests_list, 10)
    try:
        pending_requests = paginator.page(page)
    except PageNotAnInteger:
        pending_requests = paginator.page(1)
    except EmptyPage:
        pending_requests = paginator.page(paginator.num_pages)

    return render(request, 'purchase/requests_pending.html', {'pending_requests': pending_requests})


@login_required
def requests_previous(request):
    """View function that renders list of purchase forms previously approved by current user."""
    current_employee = request.user.employee_set.all()[0]
    previous_requests_list_hod = PurchaseIndentRequest.objects.none()
    previous_requests_list_jao = PurchaseIndentRequest.objects.none()
    previous_requests_list_dr = PurchaseIndentRequest.objects.none()

    if Department.objects.filter(hod=current_employee).exists():
        subordinates = current_employee.department.employee_set.values_list('id', flat=True)
        previous_requests_list_hod = PurchaseIndentRequest.objects.filter(
            state__in=['Approved by Head of Department',
                       'Approved by Junior Accounts Officer',
                       'Approved by Deputy Registrar',
                       'Rejected'],
            indenter_id__in=subordinates
        )

    if request.user.groups.filter(name='JrAO_AccountsDepartment').exists():
        previous_approved_ids = TransitionHistory.objects.filter(
            from_state='Approved by Head of Department'
        ).values_list('form_id', flat=True)
        previous_requests_list_jao = PurchaseIndentRequest.objects.filter(
            id__in=previous_approved_ids
        )

    if request.user.groups.filter(name='DR_AccountsDepartment').exists():
        previous_approved_ids = TransitionHistory.objects.filter(
            from_state='Approved by Junior Accounts Officer'
        ).values_list('form_id', flat=True)
        previous_requests_list_dr = PurchaseIndentRequest.objects.filter(
            id__in=previous_approved_ids
        )

    # Merge different forms accssible via different possible roles, take distinct and sort
    previous_requests_list = (previous_requests_list_hod | previous_requests_list_jao |
                              previous_requests_list_dr).distinct().order_by('-created_at')

    page = request.GET.get('page')
    paginator = Paginator(previous_requests_list, 10)
    try:
        previous_requests = paginator.page(page)
    except PageNotAnInteger:
        previous_requests = paginator.page(1)
    except EmptyPage:
        previous_requests = paginator.page(paginator.num_pages)

    return render(request, 'purchase/requests_previous.html', {'previous_requests': previous_requests})
