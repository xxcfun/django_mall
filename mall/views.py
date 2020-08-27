from django.shortcuts import render

# Create your views here.
from mall.models import Product
from utils import constants


def product_list(request):
    """商品列表"""
    prod_list = Product.objects.filter(status=constants.PRODUCT_STATUS_SELL, is_valid=True)
    # 按名称搜索
    name = request.GET.get('name', '')
    if name:
        prod_list = prod_list.filter(name__icontains=name)
    return render(request, 'product_list.html', {
        'prod_list': prod_list
    })


def product_detail(request, template_name='product_detail.html'):
    """商品详情"""
    return render(request, template_name)
