from django.conf.urls import url
from .views import index, requests_pending, requests_previous, submissions

app_name = 'booking'

urlpatterns = [
    url(r'^$', index.booking_index, name='booking-index'),
    url(r'^submissions', submissions.booking_submissions, name='booking-submissions'),
    url(r'^requests/pending', requests_pending.booking_requests_pending, name='booking-requests-pending'),
    url(r'^requests/previous', requests_previous.booking_requests_previous, name='booking-requests-previous'),
]