from django.contrib import admin

# Register your models here.
from mall.forms import ProductAdminForm
from mall.models import Product, Classify, Tag
from utils.admin_actions import set_invalid, set_valid


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """商品信息管理"""
    list_display = ('name', 'types', 'price', 'status', 'is_valid')
    # 修改分页数据的大小
    list_per_page = 5
    list_filter = ('status', )
    # 排除掉某些字段，使之不能编辑，在编辑界面不可见
    # exclude = ['ramain_count']
    # 不可编辑，界面可见
    readonly_fields = ['ramain_count']
    actions = [set_invalid, set_valid]
    # 添加自定义的表单
    form = ProductAdminForm


@admin.register(Classify)
class ClassifyAdmin(admin.ModelAdmin):
    """商品分类管理"""
    list_display = ('parent', 'name', 'code', 'is_valid')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """商品标签管理"""
    list_display = ('name', 'code', 'is_valid')





