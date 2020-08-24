from django.contrib import admin

# Register your models here.
from mall.models import Product, Classify, Tag


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # fields = ('name', 'types',
    #           'price', 'desc',
    #           'content', 'img',
    #           'buy_link', 'status',
    #           ('sku_count', 'ramain_count'),
    #           )
    pass


@admin.register(Classify)
class ClassifyAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass





