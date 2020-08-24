from django.conf.urls import url

from accounts import views

urlpatterns = [
    url(r'^user/login/$', views.user_login, name='user_login'),
    url(r'^user/register/$', views.user_register, name='user_register'),
]