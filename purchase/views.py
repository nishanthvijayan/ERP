from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django_fsm import can_proceed

from purchase.models import PurchaseIndentRequest
from purchase.forms import PurchaseIndentRequestForm, PurchaseIndentBudgetDetailsForm


def index(request):
    """View function that renders list of purchase list."""
    return render(request, 'purchase/index.html')


def submissions(request):
    """View function that renders current users purchase related form submissions."""
    submissions_list = PurchaseIndentRequest.objects.all()
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
    pending_requests_list = PurchaseIndentRequest.objects.all()
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
    previous_requests_list = PurchaseIndentRequest.objects.all()
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
    return render(request, 'purchase/show.html', {'purchase_indent_request': purchase_indent_request})


def purchase_indent_approve(request, request_id):
    """View function that displays current state of a form instance for approval."""
    purchase_indent_request = get_object_or_404(PurchaseIndentRequest, pk=request_id)

    if purchase_indent_request.state == 'Submitted':
        return render(request, 'purchase/show_hod.html', {'purchase_indent_request': purchase_indent_request})

    elif purchase_indent_request.state == 'Approved by Head of Department':
        form = PurchaseIndentBudgetDetailsForm()
        print form.as_p()
        return render(request, 'purchase/show_jao.html',
                      {'purchase_indent_request': purchase_indent_request, 'form': form})

    elif purchase_indent_request.state == 'Approved by Junior Accounts Officer':
        return render(request, 'purchase/show_dr.html', {'purchase_indent_request': purchase_indent_request})

    elif purchase_indent_request.state == 'Approved by Deputy Registrar':
        return render(request, 'purchase/show.html', {'purchase_indent_request': purchase_indent_request})

    elif purchase_indent_request.state == 'Rejected':
        return render(request, 'purchase/show.html', {'purchase_indent_request': purchase_indent_request})


def purchase_indent_reject(request, request_id):
    """View function that handles rejecting a form."""
    purchase_indent_request = get_object_or_404(PurchaseIndentRequest, pk=request_id)
    if not can_proceed(purchase_indent_request.hod_approve):
        raise PermissionDenied
    purchase_indent_request.hod_approve()
    purchase_indent_request.save()
    return redirect('purchase:purchase-requests-pending')


def purchase_indent_hod_approve(request, request_id):
    """View function that handles approving a form instance by HOD."""
    purchase_indent_request = get_object_or_404(PurchaseIndentRequest, pk=request_id)
    if not can_proceed(purchase_indent_request.hod_approve):
        raise PermissionDenied
    purchase_indent_request.hod_approve()
    purchase_indent_request.save()
    return redirect('purchase:purchase-requests-pending')


def purchase_indent_jao_approve(request, request_id):
    """View function that handles approving a form instance by JAO."""
    purchase_indent_request = get_object_or_404(PurchaseIndentRequest, pk=request_id)
    form = PurchaseIndentBudgetDetailsForm(request.POST, instance=purchase_indent_request)
    if form.is_valid():
        if not can_proceed(purchase_indent_request.jao_approve):
            raise PermissionDenied
        purchase_indent_request.jao_approve()
        purchase_indent_request.save()
        return redirect('purchase:purchase-requests-pending')
    else:
        return render(request, 'purchase/show_jao.html',
                      {'purchase_indent_request': purchase_indent_request}, {'form': form})


def purchase_indent_dr_approve(request, request_id):
    """View function that handles approving a form instance by DR."""
    purchase_indent_request = get_object_or_404(PurchaseIndentRequest, pk=request_id)
    if not can_proceed(purchase_indent_request.dr_approve):
        raise PermissionDenied
    purchase_indent_request.dr_approve()
    purchase_indent_request.save()
    return redirect('purchase:purchase-requests-pending')
