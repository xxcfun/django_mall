from django.conf.urls import url

from mall import views

urlpatterns = [
    # 商品列表
    url(r'^prod/list/$', views.product_list, name='product_list'),
    # 商品详情
    url(r'^prod/detail/(?P<pk>\S+)/$', views.product_detail, name='product_detail'),
]