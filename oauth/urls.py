from django.conf.urls import url

from oauth import views

urlpatterns = [
    url(r'^templ/filter/mine/$', views.templ_filter_mine, name='templ_filter_mine')
]