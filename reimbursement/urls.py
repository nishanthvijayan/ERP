from django.conf.urls import url
from . import views

app_name = 'reimbursement'

urlpatterns = [
    url(r'^$', views.reimbursement_index, name='reimbursement-index'),
    url(r'^submissions', views.reimbursement_submissions, name='reimbursement-submissions'),
    url(r'^requests/pending', views.reimbursement_requests_pending, name='reimbursement-requests-pending'),
    url(r'^requests/previous', views.reimbursement_requests_previous, name='reimbursement-requests-previous'),

    url(r'^medical/(?P<medical_id>[0-9]+)/$', views.medical.show, name='medical-show'),
]
# url(r'^form/new/$', views.new, name='medical-new'),
# url(r'^form/(?P<workflow_id>[0-9]+)/state/change$', views.state_change, name='medical-state-change'),
# ]
