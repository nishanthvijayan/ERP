from django.conf.urls import url
import views

app_name = 'home'

urlpatterns = [
    url(r'^$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),

    url(r'^users/$', views.user_index, name='user-index'),
    url(r'^users/new/$', views.user_new, name='user-new'),
    url(r'^users/(?P<user_id>\d+)/edit/$', views.user_edit, name='user-edit'),
    url(r'^users/(?P<user_id>\d+)/delete/$', views.user_delete, name='user-delete'),

    url(r'^groups/$', views.group_index, name='group-index'),
    url(r'^groups/new/$', views.group_new, name='group-new'),
    url(r'^groups/(?P<group_id>\d+)/$', views.group_show, name='group-show'),
    url(r'^groups/(?P<group_id>\d+)/edit/$', views.group_edit, name='group-edit'),
    url(r'^groups/(?P<group_id>\d+)/delete/$', views.group_delete, name='group-delete'),
    url(r'^groups/(?P<group_id>\d+)/edit/user-toggle/$', views.group_user_toggle, name='group-user-toggle'),
]
