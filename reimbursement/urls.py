from django.conf.urls import url
from . import views

app_name = 'reimbursement'

urlpatterns = [
    url(r'^$', views.reimbursement_index, name='reimbursement-index'),
    url(r'^tracking', views.reimbursement_track, name='reimbursement-track'),
    url(r'^history', views.reimbursement_history, name='reimbursement-history'),
]
