from django.conf.urls import url

from .views import index,requests_pending,requests_previous,submissions
from views.travel_allowance_advance.show import show as travel_allowance_advance_show

app_name = 'advance_allowance'

urlpatterns = [
    url(r'^$', index.advance_allowance_index, name='advance-allowance-index'),
    url(r'^submissions', submissions.advance_allowance_submissions, name='advance-allowance-submissions'),
    url(r'^requests/pending', requests_pending.advance_allowance_requests_pending, name='advance-allowance-requests-pending'),
    url(r'^requests/previous', requests_previous.advance_allowance_requests_previous, name='advance-allowance-requests-previous'),

    url(r'^travel-allowance-advance/(?P<travel_allowance_advance_id>[0-9]+)/$', travel_allowance_advance_show,
        name='travel-allowance-advance-show'),
]