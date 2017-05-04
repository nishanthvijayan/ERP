from django.conf.urls import url
from . import views

app_name = 'purchase'

urlpatterns = [
    url(r'^$', views.index, name='purchase-index'),
    url(r'^submissions', views.submissions, name='purchase-submissions'),
    url(r'^requests/pending', views.requests_pending, name='purchase-requests-pending'),
    url(r'^requests/previous', views.requests_previous, name='purchase-requests-previous'),
    url(r'^new', views.purchase_indent_new, name='purchase-indent-new'),
    url(r'^requests/(?P<request_id>[0-9]+)/$', views.purchase_indent_show, name='purchase-indent-show'),
    url(r'^requests/(?P<request_id>[0-9]+)/approve$', views.purchase_indent_approve, name='purchase-indent-approve'),
    url(r'^requests/(?P<request_id>[0-9]+)/approve_hod$', views.purchase_indent_hod_approve, name='purchase-indent-hod-approve'),
    url(r'^requests/(?P<request_id>[0-9]+)/approve_jao$', views.purchase_indent_jao_approve, name='purchase-indent-jao-approve'),
    url(r'^requests/(?P<request_id>[0-9]+)/approve_dr$', views.purchase_indent_dr_approve, name='purchase-indent-dr-approve'),
]
