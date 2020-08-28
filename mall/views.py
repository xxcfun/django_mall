from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

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


class ProductList(ListView):
    """商品列表"""
    # 每页放多少条数据
    paginate_by = 6
    # 模板位置
    template_name = 'product_list.html'

    def get_queryset(self):
        query = Q(status=constants.PRODUCT_STATUS_SELL, is_valid=True)
        # 按名称搜索
        name = self.request.GET.get('name', '')
        if name:
            query = query & Q(name__icontains=name)
        return Product.objects.filter(query)

    def get_context_data(self, **kwargs):
        """添加额外的参数，添加搜索参数"""
        context = super().get_context_data(**kwargs)
        context['search_data'] = self.request.GET.dict()
        return context
