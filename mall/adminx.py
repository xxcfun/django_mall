import xadmin

from mall.models import Product


class ProductAdmin(object):
    """xadmin商品管理"""
    list_display = ('name', 'types', 'price')
    # 快捷搜索
    list_filter = ('types', 'status')
    # 按关键字搜索
    search_fields = ('name', )

# 注册到xadmin后台管理
xadmin.site.register(Product, ProductAdmin)

