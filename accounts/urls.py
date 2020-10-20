from django.conf.urls import url

from accounts import views

urlpatterns = [
    # 用户登录
    url(r'^user/login/$', views.user_login, name='user_login'),
    # 用户登出
    url(r'^user/logout/$', views.user_logout, name='user_logout'),
    # 用户注册
    url(r'^user/register/$', views.user_register, name='user_register'),
    # 地址列表
    url(r'^user/address/list/$', views.address_list, name='address_list'),
    # 地址的修改和编辑
    # user/address/edit/add/   user/address/edit/11/
    url(r'^user/address/edit/(?P<pk>\S+)/$', views.address_edit, name='address_edit'),
    # 地址的删除
    # url(r'^user/address/delete/(?P<pk>\d+)/$', views.address_delete, name='address_delete'),
]