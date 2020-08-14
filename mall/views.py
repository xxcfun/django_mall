from django.shortcuts import render

# Create your views here.


def product_list(request, template_name='product_list.html'):
    """商品列表"""
    return render(request, template_name)


def product_detail(request, template_name='product_detail.html'):
    """商品详情"""
    return render(request, template_name)
