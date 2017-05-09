from django.contrib import admin

from .models.medical import Medical
from .models.medical import MedicalTransitionHistory
from .models.medical.general_detail import GeneralDetail
from .models.medical.amount_detail import AmountDetail
from .models.medical.medical_detail import Injection, SpecialistConsultation, Medicine, Consultation, MedicalBill,\
    MedicalDetail

from .models.telephone_expense.telephone_expense import TelephoneExpense
from .models.telephone_expense.bill.bill_detail import BillDetail
from .models.telephone_expense.bill.bill_image import BillImage
from .models.telephone_expense.telephone_expense_transition_history import TelephoneExpenseTransitionHistory


# Medical Expenses Reimbursements
admin.site.register(Medical)
admin.site.register(MedicalTransitionHistory)
admin.site.register(GeneralDetail)
admin.site.register(AmountDetail)
admin.site.register(Consultation)
admin.site.register(SpecialistConsultation)
admin.site.register(Medicine)
admin.site.register(Injection)
admin.site.register(MedicalBill)
admin.site.register(MedicalDetail)

# Telephone Expenses Reimbursements
admin.site.register(TelephoneExpense)
admin.site.register(BillDetail)
admin.site.register(BillImage)
admin.site.register(TelephoneExpenseTransitionHistory)
