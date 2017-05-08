from django.shortcuts import render, redirect
from django.contrib import messages
from django.forms import modelformset_factory
from django.db import transaction, IntegrityError

from erp_core.models.employee import Employee

from reimbursement.models.telephone_expense.telephone_expense import TelephoneExpense
from reimbursement.models.telephone_expense.bill.bill_detail import BillDetail
from reimbursement.models.telephone_expense.bill.bill_image import BillImage

from reimbursement.forms.telephone_expense.bill.bill_detail import BillDetailForm
from reimbursement.forms.telephone_expense.bill.bill_image import BillImageForm


def telephone_expense_new(request):
    bill_detail_modelformset = modelformset_factory(
        BillDetail,
        form=BillDetailForm,
    )
    bill_image_modelformset = modelformset_factory(
        BillImage,
        form=BillImageForm,
    )
    if request.method == 'POST':

        bill_detail_formset = bill_detail_modelformset(
            data=request.POST,
            prefix="bill-detail-formset",
            queryset=BillDetail.objects.none()
        )
        bill_image_formset = bill_image_modelformset(
            data=request.POST,
            files=request.FILES,
            prefix="bill-image-formset",
            queryset=BillImage.objects.none()
        )

        if bill_detail_formset.is_valid() and bill_image_formset.is_valid():

            try:
                with transaction.atomic():

                    employee = Employee.objects.filter(user_id=request.user.id).first()

                    telephone_expense = TelephoneExpense.objects.create(employee=employee)
                    telephone_expense.save()

                    for bill_detail_form in bill_detail_formset:
                        if bill_detail_form.has_changed():
                            bill_detail_form_obj = bill_detail_form.save(commit=False)
                            bill_detail_form_obj.telephone_expense = telephone_expense
                            bill_detail_form_obj.save()

                    for bill_image_form in bill_image_formset:
                        if bill_image_form.has_changed():
                            bill_image_form_obj = bill_image_form.save(commit=False)
                            bill_image_form_obj.telephone_expense = telephone_expense
                            bill_image_form_obj.save()

                    messages.success(request, 'New telephone expense reimbursement'
                                     + ' request submitted successfully with ID #'
                                     + str(telephone_expense.id))
                    return redirect('reimbursement:telephone-expense-show', telephone_expense.id)

            except IntegrityError:  # If the transaction failed
                messages.error(request, 'There was an error submitting your reimbursement request.')

        else:
            messages.error(request, 'Please resolve below issues')
    else:
        bill_detail_formset = bill_detail_modelformset(
            prefix="bill-detail-formset",
            queryset=BillDetail.objects.none()
        )
        bill_image_formset = bill_image_modelformset(
            prefix="bill-image-formset",
            queryset=BillImage.objects.none()
        )

    context = {
        'bill_detail_formset': bill_detail_formset,
        'bill_image_formset': bill_image_formset
    }

    return render(request, 'reimbursement/telephone_expense/new.html', context)
