from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum, Q
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.views.generic import DetailView

from mall.models import Product
from mine.models import Order, Cart
from utils import constants, tools


class OrderDetailView(DetailView):
    """订单详情"""
    model = Order
    slug_field = 'sn'
    slug_url_kwarg = 'sn'
    template_name = 'order_info.html'


@login_required
@transaction.atomic()
def cart_add(request, prod_uid):
    """添加商品到购物车"""
    product = get_object_or_404(Product, uid=prod_uid, is_valid=True, status=constants.PRODUCT_STATUS_SELL)
    # 购买数量
    count = int(request.POST.get('count', 1))
    # 校验库存
    if product.ramain_count < count:
        return HttpResponse('no')
    # 减库存
    product.update_store_count(count)
    # 生成购物车记录
    # 如果已经添加到购物车了，就把购买的数量和价格更新一下
    try:
        cart = Cart.objects.get(product=product, user=request.user, status=constants.ORDER_STATUS_INIT)
        count = cart.count + count
        cart.count = count
        cart.amount = count * cart.price
        cart.save()
    except Cart.DoesNotExist:
        # 没有加入过购物车
        Cart.objects.create(
            product=product,
            user=request.user,
            name=product.name,
            img=product.img,
            price=product.price,
            origin_price=product.origin_price,
            count=count,
            amount=count * product.price
        )

    return HttpResponse('ok')


@login_required
def cart(request):
    """我的购物车"""
    user = request.user
    # 我购物车中的商品列表
    prod_list = request.user.carts.filter(status=constants.ORDER_STATUS_INIT)
    # 聚合查询
    if request.method == 'POST':
        # 提交订单
        # 1 保存用户的地址快照
        default_addr = user.default_addr
        if not default_addr:
            # 消息通知
            messages.warning(request, '请选择地址信息')
            return redirect('accounts:address_list')
        # 订单总额计算
        cart_total = prod_list.aggregate(sum_amount=Sum('amount'), sum_count=Sum('count'))
        order = Order.objects.create(
            user=user,
            sn=tools.gen_trans_id(),
            buy_amount=cart_total['sum_amount'],
            buy_count=cart_total['sum_count'],
            to_user=default_addr.username,
            to_area=default_addr.get_region_format(),
            to_address=default_addr.address,
            to_phone=default_addr.phone,
        )
        # 2 修改购物车中的状态 已提交
        # 3 生成订单，关联到购物车
        prod_list.update(
            status=constants.ORDER_STATUS_SUBMIT,
            order=order
        )
        # 4 跳转到订单详情
        messages.success(request, '下单成功，请支付')
        return redirect('mine:order_detail', order.sn)

    return render(request, 'cart.html', {
        'prod_list': prod_list
    })


@login_required()
def order_pay(request):
    """提交订单"""
    user = request.user
    if request.method == 'POST':
        sn = request.POST.get('sn', None)
        # 1 查询订单信息
        order = get_object_or_404(Order, sn=sn, user=user)
        # 2 验证钱够不够
        if order.buy_amount > user.integral:
            messages.error(request, '积分余额不足')
            return redirect('mine:order_detail', sn=sn)
        # 3 钱扣掉
        user.ope_integral_account(0, order.buy_amount)
        # 4 修改订单状态
        order.status = constants.ORDER_STATUS_PAIED
        order.save()
        # 5 修改购物车关联的状态
        order.carts.all().update(status=constants.ORDER_STATUS_PAIED)
        messages.success(request, '支付成功')
    return redirect('mine:order_detail', sn=sn)
