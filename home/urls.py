from django.conf.urls import url
import views

app_name='home'

urlpatterns = [
    url(r'^$', views.LoginView.as_view(), name='login'),
    url(r'^logout$', views.LogoutView.as_view(), name='logout'),

    url(r'^home$', views.home, name='home'),
    url(r'^users/register$', views.user_register, name='user-register'),
    url(r'^users/(?P<user_id>\d+)/edit$', views.user_edit, name='user-edit'),
    url(r'^users/(?P<user_id>\d+)/remove$', views.user_remove, name='user-remove'),

    url(r'^groups$', views.group_index, name='group-index'),
    url(r'^groups/create$', views.group_create, name='group-create'),
    url(r'^groups/(?P<group_id>\d+)$', views.group_show, name='group-show'),
    url(r'^groups/(?P<group_id>\d+)/edit$', views.group_edit, name='group-edit'),
    url(r'^groups/(?P<group_id>\d+)/delete$', views.group_delete, name='group-delete'),
    url(r'^groups/(?P<group_id>\d+)/edit/user-toggle$', views.group_user_toggle, name='group-user-toggle'),
]
