from django.conf.urls import url
from . import views

app_name = 'forms'

urlpatterns = [
    url(r'^$', views.workflow_index, name='workflow-index'),
    url(r'^workflows/(?P<workflow_id>[0-9]+)/$', views.workflow_show, name='workflow-show'),
    url(r'^workflows/(?P<workflow_id>[0-9]+)/edit$', views.workflow_edit, name='workflow-edit'),
    url(r'^workflows/new$', views.workflow_new, name='workflow-new'),
    url(r'^workflows/(?P<workflow_id>[0-9]+)/delete$', views.workflow_delete, name='workflow-delete'),

    url(r'^workflows/(?P<workflow_id>[0-9]+)/elements/new$', views.form_element_new, name='form-element-new'),
    url(r'^workflows/(?P<workflow_id>[0-9]+)/elements/(?P<element_id>[0-9]+)/edit$',
        views.form_element_edit, name='form-element-edit'),
    url(r'^workflows/(?P<workflow_id>[0-9]+)/elements/(?P<element_id>[0-9]+)/delete$',
        views.form_element_delete, name='form-element-delete'),

    url(r'^workflows/(?P<workflow_id>[0-9]+)/states/new$', views.state_new, name='state-new'),
    url(r'^workflows/(?P<workflow_id>[0-9]+)/states/(?P<state_id>[0-9]+)/edit$', views.state_edit, name='state-edit'),
    url(r'^workflows/(?P<workflow_id>[0-9]+)/states/(?P<state_id>[0-9]+)/delete$',
        views.state_delete, name='state-delete'),

    url(r'^workflows/(?P<workflow_id>[0-9]+)/transitions/new$', views.transition_new, name='transition-new'),
    url(r'^workflows/(?P<workflow_id>[0-9]+)/transitions/(?P<transition_id>[0-9]+)/edit$',
        views.transition_edit, name='transition-edit'),
    url(r'^workflows/(?P<workflow_id>[0-9]+)/transitions/(?P<transition_id>[0-9]+)/delete$',
        views.transition_delete, name='transition-delete'),

    url(r'^workflows/(?P<workflow_id>[0-9]+)/responses/$', views.workflow_entry_index, name='workflow-entry-index'),
    url(r'^workflows/(?P<workflow_id>[0-9]+)/responses/new$', views.workflow_entry_new, name='workflow-entry-new'),
]
