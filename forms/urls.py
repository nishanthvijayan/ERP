from django.conf.urls import url
from . import views

app_name = 'forms'

urlpatterns = [
    url(r'^$', views.index, name='workflows-index'),
    url(r'^workflows/(?P<workflow_id>[0-9]+)/$', views.show, name='workflows-show'),
    url(r'^workflows/(?P<workflow_id>[0-9]+)/edit$', views.edit, name='workflows-edit'),
]