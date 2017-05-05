from django.conf.urls import url
from . import views

app_name = 'booking'

urlpatterns = [
    url(r'^$', views.booking_index, name='booking-index'),
    url(r'^submissions', views.booking_submissions, name='booking-submissions'),
    url(r'^requests/pending', views.booking_requests_pending, name='booking-requests-pending'),
    url(r'^requests/previous', views.booking_requests_previous, name='booking-requests-previous'),
]