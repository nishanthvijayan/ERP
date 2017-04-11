from django.conf.urls import url
from . import views

app_name = 'reimbursement'

urlpatterns = [
    url(r'^$', views.reimbursement_index, name='reimbursement-index'),
    url(r'^tracking', views.reimbursement_tracking, name='reimbursement-tracking'),
    url(r'^history', views.reimbursement_history, name='reimbursement-history'),
]
