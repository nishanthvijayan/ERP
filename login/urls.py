from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.LoginView.as_view(), name='login'),
    url(r'^home/{0,1}$', views.home, name='home'),
    url(r'^invalid/{0,1}$', views.invalid, name='invalid_login'),
    url(r'^logout/{0,1}$', views.LogoutView.as_view(), name='loggedout'),
    url(r'^register-user/{0,1}$', views.register_user, name='register-user'),
    url(r'^remove-user/(?P<username>[0-9a-zA-Z@\.\+\-_]{1,150})/{0,1}$', views.remove_user, name='remove-user'),
    url(r'^edit-user/(?P<username>[0-9a-zA-Z@\.\+\-_]{1,150})/{0,1}$', views.edit_user, name='edit-user'),
    url(r'^create-group/{0,1}$', views.create_group, name='create-group'),
    url(r'^delete-group/(?P<name>.{1,80})/{0,1}$', views.delete_group, name='delete-group'),
    url(r'^edit-group/(?P<name>.{1,80})/(?P<task>(change-name)|(add-user)|(remove-user/([0-9a-zA-Z@\.\+\-_]{1,150})))/{0,1}$', views.edit_group, name='edit-group'),
    url(r'^show-group/(?P<name>.{1,80})/{0,1}$', views.show_group, name='show-group'),
]