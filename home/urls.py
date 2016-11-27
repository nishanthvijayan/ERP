from django.conf.urls import url
import views

app_name = 'home'

urlpatterns = [
    url(r'^$', views.LoginView.as_view(), name='login'),
    url(r'^home/$', views.HomeView.as_view(), name='home'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
]
