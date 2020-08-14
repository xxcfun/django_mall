from django.conf.urls import url

from system import views

urlpatterns = [
    url(r'^news/$', views.news_list, name='news_list'),
    url(r'^new/(?P<pk>\d+)/$', views.news_detail, name='news_detail'),
]