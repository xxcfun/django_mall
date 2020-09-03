from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from accounts.models import User, UserProfile, UserAddress


@admin.register(User)
class UserAdmin(UserAdmin):
    """用户管理"""
    list_display = ('format_username', 'nickname', 'integral', 'is_active')
    # 支持按用户名、昵称进行搜索
    search_fields = ('username', 'nickname')
    # 添加自定义的方法
    actions = ['disable_user', 'enable_user']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name', 'email',
                                        'integral', 'level', 'nickname')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    def format_username(self, obj):
        """用户名脱敏处理"""
        return obj.username[0:3] + '***'
    # 修改列明显示
    format_username.short_description = '用户名'

    def disable_user(self, request, queryset):
        """批量禁用选中的用户"""
        queryset.update(is_active=False)
    disable_user.short_description = "批量禁用用户"

    def enable_user(self, request, queryset):
        """批量启用选中的用户"""
        queryset.update(is_active=True)
    enable_user.short_description = "批量启用用户"


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """用户详细信息"""
    list_display = ('user', 'phone_no', 'sex')


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    """用户地址管理"""
    list_display = ('user', 'province', 'city',
                    'username', 'address', 'phone',
                    'is_valid', 'is_default')
    search_fields = ('user__username', 'user__nickname',
                     'username', 'phone')
