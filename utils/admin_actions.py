from django.contrib import messages


def set_invalid(modeladmin, request, queryset):
    """批量禁用 is_valid=False"""
    queryset.update(is_valid=False)
    messages.success(request, '操作成功')

set_invalid.short_description = '禁用所选对象'


def set_valid(modeladmin, request, queryset):
    """批量启用 is_valid=True"""
    queryset.update(is_valid=True)
    messages.success(request, '操作成功')

set_valid.short_description = '启用所选对象'