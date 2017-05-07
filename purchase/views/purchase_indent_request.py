from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django_fsm import can_proceed
from django.forms.formsets import formset_factory

from purchase.models import PurchaseIndentRequest, TransitionHistory, STATE, Item, Vendor
from purchase.forms import PurchaseIndentRequestForm, PurchaseIndentBudgetDetailsForm, ItemVendorForm


def purchase_indent_new(request):
    """View function that handles new form submission."""
    ItemVendorFormSet = formset_factory(ItemVendorForm)
    if request.method == 'POST':
        form = PurchaseIndentRequestForm(request.POST, request.FILES)
        item_vendor_formset = ItemVendorFormSet(request.POST)

        if form.is_valid() and item_vendor_formset.is_valid():
            submission = form.save(commit=False)
            submission.indenter = request.user.employee_set.all()[0]
            submission.save()

            for item_form in item_vendor_formset:
                item = Item(purchase_request=submission,
                            specification=item_form.cleaned_data['specification'],
                            quantity=item_form.cleaned_data['quantity'],
                            type=item_form.cleaned_data['type'],
                            estimated_cost=item_form.cleaned_data['estimated_cost']
                            )
                item.save()
                vendor = Vendor(item=item, name=item_form.cleaned_data['vendor_name'],
                                email=item_form.cleaned_data['vendor_email'],
                                address=item_form.cleaned_data['vendor_address'])
                vendor.save()
            return redirect('purchase:purchase-submissions')
    else:
        form = PurchaseIndentRequestForm()
        item_vendor_formset = ItemVendorFormSet()

    return render(request, 'purchase/purchase_indent/new.html',
                  {'form': form, 'item_vendor_formset': item_vendor_formset})


def purchase_indent_show(request, request_id):
    """View function that displays current state of a form instance for viewing."""
    purchase_indent_request = get_object_or_404(PurchaseIndentRequest, pk=request_id)
    current_employee = request.user.employee_set.all()[0]

    # Check if logged in user is indenter, indenter's HOD, JAO or DR
    if purchase_indent_request.indenter == current_employee or \
       purchase_indent_request.indenter.department.hod_id == current_employee.id or \
       request.user.groups.filter(name__in=['JrAO_AccountsDepartment', 'DR_AccountsDepartment']).exists():
        return render(request, 'purchase/purchase_indent/show.html',
                      {'purchase_indent_request': purchase_indent_request})

    else:
        return PermissionDenied


def purchase_indent_approve(request, request_id):
    """View function that displays current state of a form instance for approval."""
    purchase_indent_request = get_object_or_404(PurchaseIndentRequest, pk=request_id)
    current_employee = request.user.employee_set.all()[0]

    if purchase_indent_request.state == 'Submitted':
        if purchase_indent_request.indenter.department.hod_id != current_employee.id:
            raise PermissionDenied
        return render(request, 'purchase/purchase_indent/show_hod.html',
                      {'purchase_indent_request': purchase_indent_request})

    elif purchase_indent_request.state == 'Approved by Head of Department':
        if not request.user.groups.filter(name='JrAO_AccountsDepartment').exists():
            raise PermissionDenied
        form = PurchaseIndentBudgetDetailsForm()

        return render(request, 'purchase/purchase_indent/show_jao.html',
                      {'purchase_indent_request': purchase_indent_request, 'form': form})

    elif purchase_indent_request.state == 'Approved by Junior Accounts Officer':
        if not request.user.groups.filter(name='DR_AccountsDepartment').exists():
            raise PermissionDenied
        return render(request, 'purchase/purchase_indent/show_dr.html',
                      {'purchase_indent_request': purchase_indent_request})

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
        return render(request, 'purchase/purchase_indent/show_jao.html',
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
