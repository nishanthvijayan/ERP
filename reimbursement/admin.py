from django.contrib import admin

from .models.medical import Medical
from .models.medical import TransitionHistory
from .models.medical.general_detail import GeneralDetail
from .models.medical.amount_detail import AmountDetail
from .models.medical.medical_detail import Injection, SpecialistConsultation, Medicine, Consultation, MedicineBill,\
    MedicalDetail

from .models.telephone_expense.telephone_expense import TelephoneExpenses


# Medical Expenses Reimbursements
admin.site.register(Medical)
admin.site.register(TransitionHistory)
admin.site.register(GeneralDetail)
admin.site.register(AmountDetail)
admin.site.register(Consultation)
admin.site.register(SpecialistConsultation)
admin.site.register(Medicine)
admin.site.register(Injection)
admin.site.register(MedicineBill)
admin.site.register(MedicalDetail)

# Telephone Expenses Reimbursements
admin.site.register(TelephoneExpenses)
