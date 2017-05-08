from django.conf.urls import url
from .views import index, requests_pending, requests_previous, submissions
from views.mp_hall.show import show as mp_hall_show
from views.mp_hall.new import new as mp_hall_new
from views.mp_hall.state_change.state_change import state_change as mp_hall_state_change

app_name = 'booking'

urlpatterns = [
    url(r'^$', index.booking_index, name='booking-index'),
    url(r'^submissions', submissions.booking_submissions, name='booking-submissions'),
    url(r'^requests/pending', requests_pending.booking_requests_pending, name='booking-requests-pending'),
    url(r'^requests/previous', requests_previous.booking_requests_previous, name='booking-requests-previous'),
    url(r'^mp-hall/(?P<mp_hall_id>[0-9]+)/$', mp_hall_show, name='mp-hall-show'),
    url(r'^mp-hall/new/$', mp_hall_new, name='mp-hall-new'),
    url(r'^mp-hall/(?P<mp_hall_id>[0-9]+)/state-change$', mp_hall_state_change, name='mp-hall-state-change')

]