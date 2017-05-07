from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django_fsm import can_proceed

from erp_core.models import Department
from purchase.models import PurchaseIndentRequest, TransitionHistory, STATE
from purchase.forms import PurchaseIndentRequestForm, PurchaseIndentBudgetDetailsForm


def index(request):
    """View function that renders list of purchase list."""
    return render(request, 'purchase/index.html')


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


def requests_pending(request):
    """View function that renders list of purchase forms pending current user's approval."""
    current_employee = request.user.employee_set.all()[0]

    if Department.objects.filter(hod=current_employee).exists():
        subordinates = current_employee.department.employee_set.values_list('id', flat=True)
        pending_requests_list = PurchaseIndentRequest.objects.filter(state='Submitted', indenter_id__in=subordinates)
    elif request.user.groups.filter(name='JrAO_AccountsDepartment').exists():
        pending_requests_list = PurchaseIndentRequest.objects.filter(state='Approved by Head of Department')
    elif request.user.groups.filter(name='DR_AccountsDepartment').exists():
        pending_requests_list = PurchaseIndentRequest.objects.filter(state='Approved by Junior Accounts Officer')
    else:
        pending_requests_list = PurchaseIndentRequest.objects.none()

    page = request.GET.get('page')
    paginator = Paginator(pending_requests_list, 10)
    try:
        pending_requests = paginator.page(page)
    except PageNotAnInteger:
        pending_requests = paginator.page(1)
    except EmptyPage:
        pending_requests = paginator.page(paginator.num_pages)

    return render(request, 'purchase/requests_pending.html', {'pending_requests': pending_requests})


def requests_previous(request):
    """View function that renders list of purchase forms previously approved by current user."""
    current_employee = request.user.employee_set.all()[0]

    if Department.objects.filter(hod=current_employee).exists():
        subordinates = current_employee.department.employee_set.values_list('id', flat=True)
        previous_requests_list = PurchaseIndentRequest.objects.filter(
            state__in=['Approved by Head of Department',
                       'Approved by Junior Accounts Officer',
                       'Approved by Deputy Registrar',
                       'Rejected'],
            indenter_id__in=subordinates
        )

    elif request.user.groups.filter(name='JrAO_AccountsDepartment').exists():
        previous_approved_ids = TransitionHistory.objects.filter(
            from_state='Approved by Head of Department'
        ).values_list('form_id', flat=True)
        previous_requests_list = PurchaseIndentRequest.objects.filter(
            id__in=previous_approved_ids
        )

    elif request.user.groups.filter(name='DR_AccountsDepartment').exists():
        previous_approved_ids = TransitionHistory.objects.filter(
            from_state='Approved by Junior Accounts Officer'
        ).values_list('form_id', flat=True)
        previous_requests_list = PurchaseIndentRequest.objects.filter(
            id__in=previous_approved_ids
        )

    else:
        previous_requests_list = PurchaseIndentRequest.objects.none()

    page = request.GET.get('page')
    paginator = Paginator(previous_requests_list, 10)
    try:
        previous_requests = paginator.page(page)
    except PageNotAnInteger:
        previous_requests = paginator.page(1)
    except EmptyPage:
        previous_requests = paginator.page(paginator.num_pages)

    return render(request, 'purchase/requests_previous.html', {'previous_requests': previous_requests})


def purchase_indent_new(request):
    """View function that handles new form submission."""
    if request.method == 'POST':
        form = PurchaseIndentRequestForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.indenter = request.user.employee_set.all()[0]
            submission.save()
            return redirect('purchase:purchase-submissions')
    else:
        form = PurchaseIndentRequestForm()

    return render(request, 'purchase/new.html', {'form': form})


def purchase_indent_show(request, request_id):
    """View function that displays current state of a form instance for viewing."""
    purchase_indent_request = get_object_or_404(PurchaseIndentRequest, pk=request_id)
    current_employee = request.user.employee_set.all()[0]

    # Check if logged in user is indenter, indenter's HOD, JAO or DR
    if purchase_indent_request.indenter == current_employee or \
       purchase_indent_request.indenter.department.hod_id == current_employee.id or \
       request.user.groups.filter(name__in=['JrAO_AccountsDepartment', 'DR_AccountsDepartment']).exists():
        return render(request, 'purchase/show.html', {'purchase_indent_request': purchase_indent_request})

    else:
        return PermissionDenied


def purchase_indent_approve(request, request_id):
    """View function that displays current state of a form instance for approval."""
    purchase_indent_request = get_object_or_404(PurchaseIndentRequest, pk=request_id)
    current_employee = request.user.employee_set.all()[0]

    if purchase_indent_request.state == 'Submitted':
        if purchase_indent_request.indenter.department.hod_id != current_employee.id:
            raise PermissionDenied
        return render(request, 'purchase/show_hod.html', {'purchase_indent_request': purchase_indent_request})

    elif purchase_indent_request.state == 'Approved by Head of Department':
        if not request.user.groups.filter(name='JrAO_AccountsDepartment').exists():
            raise PermissionDenied
        form = PurchaseIndentBudgetDetailsForm()

        return render(request, 'purchase/show_jao.html',
                      {'purchase_indent_request': purchase_indent_request, 'form': form})

    elif purchase_indent_request.state == 'Approved by Junior Accounts Officer':
        if not request.user.groups.filter(name='DR_AccountsDepartment').exists():
            raise PermissionDenied
        return render(request, 'purchase/show_dr.html', {'purchase_indent_request': purchase_indent_request})

    else:
        return PermissionDenied


def purchase_indent_hod_approve(request, request_id):
    """View function that handles approving a form instance by HOD."""
    current_employee = request.user.employee_set.all()[0]
    purchase_indent_request = get_object_or_404(PurchaseIndentRequest, pk=request_id)

    # Check if logged in user is indenter's HOD
    if purchase_indent_request.indenter.department.hod_id != current_employee.id:
        raise PermissionDenied

    if request.POST.get('Approve'):
        if not can_proceed(purchase_indent_request.hod_approve):
            raise PermissionDenied

        purchase_indent_request.hod_approve()
        purchase_indent_request.save()

        remark = request.POST.get('remark')
        transition_record = TransitionHistory(
            approver=current_employee,
            form=purchase_indent_request,
            from_state=STATE.SUBMITTED,
            to_state=STATE.APPROVED_BY_HOD,
            remark=remark
        )
        transition_record.save()

    elif request.POST.get('Reject'):
        if not can_proceed(purchase_indent_request.reject):
            raise PermissionDenied

        purchase_indent_request.reject()
        purchase_indent_request.save()

        remark = request.POST.get('remark')
        transition_record = TransitionHistory(
            approver=current_employee,
            form=purchase_indent_request,
            from_state=STATE.SUBMITTED,
            to_state=STATE.REJECT,
            remark=remark
        )
        transition_record.save()

    return redirect('purchase:purchase-requests-pending')


def purchase_indent_jao_approve(request, request_id):
    """View function that handles approving a form instance by JAO."""
    # Check if logged in user is JAO
    if not request.user.groups.filter(name='JrAO_AccountsDepartment').exists():
        raise PermissionDenied

    current_employee = request.user.employee_set.all()[0]
    purchase_indent_request = get_object_or_404(PurchaseIndentRequest, pk=request_id)
    form = PurchaseIndentBudgetDetailsForm(request.POST, instance=purchase_indent_request)

    if form.is_valid():
        if request.POST.get('Approve'):
            if not can_proceed(purchase_indent_request.jao_approve):
                raise PermissionDenied

            purchase_indent_request.jao_approve()
            purchase_indent_request.save()

            remark = request.POST.get('remark')
            transition_record = TransitionHistory(
                approver=current_employee,
                form=purchase_indent_request,
                from_state=STATE.APPROVED_BY_HOD,
                to_state=STATE.APPROVED_BY_JAO,
                remark=remark
            )
            transition_record.save()

        elif request.POST.get('Reject'):
            if not can_proceed(purchase_indent_request.reject):
                raise PermissionDenied

            purchase_indent_request.reject()
            purchase_indent_request.save()

            remark = request.POST.get('remark')
            transition_record = TransitionHistory(
                approver=current_employee,
                form=purchase_indent_request,
                from_state=STATE.APPROVED_BY_HOD,
                to_state=STATE.REJECT,
                remark=remark
            )
            transition_record.save()

        return redirect('purchase:purchase-requests-pending')
    else:
        return render(request, 'purchase/show_jao.html',
                      {'purchase_indent_request': purchase_indent_request}, {'form': form})


def purchase_indent_dr_approve(request, request_id):
    """View function that handles approving a form instance by DR."""
    # Check if logged in user is DR
    if not request.user.groups.filter(name='DR_AccountsDepartment').exists():
        raise PermissionDenied

    current_employee = request.user.employee_set.all()[0]
    purchase_indent_request = get_object_or_404(PurchaseIndentRequest, pk=request_id)

    if request.POST.get('Approve'):
        if not can_proceed(purchase_indent_request.dr_approve):
            raise PermissionDenied

        purchase_indent_request.dr_approve()
        purchase_indent_request.save()

        remark = request.POST.get('remark')
        transition_record = TransitionHistory(
            approver=current_employee,
            form=purchase_indent_request,
            from_state=STATE.APPROVED_BY_JAO,
            to_state=STATE.APPROVED_BY_DR,
            remark=remark
        )
        transition_record.save()

    elif request.POST.get('Reject'):
        if not can_proceed(purchase_indent_request.reject):
            raise PermissionDenied

        purchase_indent_request.reject()
        purchase_indent_request.save()

        remark = request.POST.get('remark')
        transition_record = TransitionHistory(
            approver=current_employee,
            form=purchase_indent_request,
            from_state=STATE.APPROVED_BY_JAO,
            to_state=STATE.REJECT,
            remark=remark
        )
        transition_record.save()

    return redirect('purchase:purchase-requests-pending')
