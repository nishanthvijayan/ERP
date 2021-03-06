from django.conf.urls import url

from . import views

app_name = 'reimbursement'

urlpatterns = [
    url(r'^$', views.reimbursement_index, name='reimbursement-index'),
    url(r'^submissions', views.reimbursement_submissions, name='reimbursement-submissions'),
    url(r'^requests/pending', views.reimbursement_requests_pending, name='reimbursement-requests-pending'),
    url(r'^requests/previous', views.reimbursement_requests_previous, name='reimbursement-requests-previous'),

    url(r'^medical/new/$', views.medical.new, name='medical-new'),
    url(r'^medical/(?P<medical_id>[0-9]+)/$', views.medical.show, name='medical-show'),
    url(r'^medical/(?P<medical_id>[0-9]+)/state-change$', views.medical.state_change, name='medical-state-change'),

    url(r'^telephone-expense/(?P<telephone_expense_id>[0-9]+)/$', views.telephone_expense.telephone_expense_show,
        name='telephone-expense-show'),
    url(r'^telephone-expense/new/$', views.telephone_expense.telephone_expense_new,
        name='telephone-expense-new'),
    url(r'^telephone-expense/(?P<telephone_expense_id>[0-9]+)/state-change/$', views.telephone_expense.state_change,
        name='telephone-expense-state-change')
]
