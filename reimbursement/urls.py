from django.conf.urls import url
from . import views

app_name = 'reimbursement'

urlpatterns = [
    url(r'^$', views.reimbursement_index, name='reimbursement-index'),
    url(r'^submissions', views.reimbursement_submissions, name='reimbursement-submissions'),
    url(r'^requests/pending', views.reimbursement_requests_pending, name='reimbursement-requests-pending'),
    url(r'^requests/previous', views.reimbursement_requests_previous, name='reimbursement-requests-previous'),
]
