from django.conf.urls import url
import views

app_name='home'

urlpatterns = [
    url(r'^$', views.LoginView.as_view(), name='login'),
    url(r'^home/{0,1}$', views.home, name='home'),
    url(r'^users/logout/{0,1}$', views.LogoutView.as_view(), name='loggedout'),
    url(r'^users/register/{0,1}$', views.register_user, name='register-user'),
    url(r'^users/(?P<user_id>\d+)/edit/{0,1}$', views.edit_user, name='edit-user'),
    url(r'^users/(?P<user_id>\d+)/remove/{0,1}$', views.remove_user, name='remove-user'),
    url(r'^groups/create/{0,1}$', views.create_group, name='create-group'),
    url(r'^groups/(?P<group_id>\d+)/{0,1}$', views.show_group, name='show-group'),
    url(r'^groups/(?P<group_id>\d+)/edit/edit-name/{0,1}$', views.edit_group_name, name='edit-group-name'),
    url(r'^groups/(?P<group_id>\d+)/edit/toggle-user/{0,1}$', views.toggle_user_group, name='toggle-user-group'),
    url(r'^groups/(?P<group_id>\d+)/delete/{0,1}$', views.delete_group, name='delete-group'),
]