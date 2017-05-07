# from django import forms
#
# from reimbursement.models.telephone_expense.telephone_expense import TelephoneExpense
#
#
# class TelephoneExpenseForm(forms.ModelForm):
#     class Meta:
#         model = TelephoneExpense
#
#     def __init__(self, *args, **kwargs):
#         super(TelephoneExpenseForm, self).__init__(*args, **kwargs)
#         for field in TelephoneExpense._meta.get_fields():
#             if field.name in self.fields:
#                 self.fields[field.name].widget.attrs = {
#                         'class': 'form-control',
#                         'placeholder': self.fields[field.name].help_text
#                     }
#
#     def save(self, commit=True):
#         telephone_expense = super(TelephoneExpenseForm, self).save(commit=False)
#         if commit:
#             telephone_expense.save()
#         return telephone_expense
