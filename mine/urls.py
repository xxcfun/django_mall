from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from mine import views

urlpatterns = [
    url(r'^$', views.mine, name='mine'),
    # 订单详情
    url(r'^order/detail/(?P<sn>\S+)/$', login_required(views.OrderDetailView.as_view()), name='order_detail'),
    # 添加到购物车
    url(r'^cart/add/(?P<prod_uid>\S+)/$', views.cart_add, name='cart_add'),
    # 我的购物车
    url(r'^cart/$', views.cart, name='cart'),
    # 提交订单
    url(r'^order/pay/$', views.order_pay, name='order_pay'),
    # 我的订单列表
    url(r'^order/list/$', login_required(views.OrderListView.as_view()), name='order_list'),
    # 我的收藏
    url(r'^prod/collect/$', views.product_collect, name='product_collect')
]
