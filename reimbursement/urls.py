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

    url(r'^telephone-expenses/new/$', views.telephone_expenses.new,
        name='telephone-expenses-new'),
    url(r'^telephone-expenses/(?P<telephone_expenses_id>[0-9]+)/$', views.telephone_expenses.show,
        name='telephone-expenses-show'),
    url(r'^telephone-expenses/(?P<telephone_expenses_id>[0-9]+)/state-change$', views.telephone_expenses.state_change,
        name='telephone-expenses-state-change'),
]
