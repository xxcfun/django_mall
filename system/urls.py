from django.conf.urls import url

from system import views

urlpatterns = [
    # 新闻列表
    url(r'^news/$', views.news_list, name='news_list'),
    # 新闻详情
    url(r'^new/(?P<pk>\d+)/$', views.news_detail, name='news_detail'),
    # 验证码
    url(r'^verify/code/$', views.verify_code, name='verify_code'),
]