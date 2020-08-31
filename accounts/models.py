from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """用户的基础信息"""
    # username = models.CharField('用户名', max_length=64)
    # password = models.CharField('密码', max_length=255)
    nickname = models.CharField('昵称', max_length=255)
    avatar = models.ImageField('用户头像', upload_to='avatar', null=True, blank=True)
    integral = models.IntegerField('用户的积分', default=0)
    level = models.SmallIntegerField('用户级别', null=True, blank=True)

    class Meta:
        db_table = 'accounts_user'
        verbose_name = '用户基础信息'
        verbose_name_plural = '用户基础信息'

    @property
    def default_addr(self):
        """用户的默认地址，在多个地方用到"""
        addr = None
        user_list = self.user_address.filter(is_valid=True)
        # UserAddress.objects.filter(user=user, is_valid=True)  上面等同于这句

        # 1 找默认地址
        try:
            addr = user_list[0]
        except IndexError:
            try:
                addr = user_list[0]
                # 2 如果没有默认地址，显示所有地址的第一个
            except IndexError:
                pass
        return addr

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    """用户详细表"""
    SEX_CHOICES = (
        (1, '男'),
        (0, '女'),
    )
    user = models.OneToOneField(User)
    real_name = models.CharField('真实姓名', max_length=32)
    email = models.CharField('电子邮箱', max_length=128, null=True, blank=True)
    is_email_valid = models.BooleanField('邮箱是否已经验证', default=False)
    phone_no = models.CharField('手机号', max_length=20, null=True, blank=True)
    is_phone_valid = models.BooleanField('是否已经验证', default=False)
    sex = models.SmallIntegerField('性别', default=1, choices=SEX_CHOICES)
    age = models.SmallIntegerField('年龄', default=0)

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        db_table = 'accounts_user_profile'
        verbose_name = '用户详细信息'
        verbose_name_plural = '用户详细信息'


class UserAddress(models.Model):
    """用户的地址信息"""
    user = models.ForeignKey(User, related_name='user_address')
    province = models.CharField('省份', max_length=32)
    city = models.CharField('市区', max_length=32)
    area = models.CharField('区域', max_length=32)
    town = models.CharField('街道', max_length=32, null=True, blank=True)

    address = models.CharField('详细地址', max_length=64)
    username = models.CharField('收件人', max_length=32)
    phone = models.CharField('收件人的电话', max_length=32)

    is_default = models.BooleanField('是否为默认地址', default=False)
    is_valid = models.BooleanField('是否有效', default=True)

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        db_table = 'accounts_user_address'
        ordering = ['is_default', '-updated_at']
        verbose_name = '用户地址信息'
        verbose_name_plural = '用户地址信息'

    def get_phone_format(self):
        """格式化手机号码显示"""
        return self.phone[0:3] + '****' + self.phone[7:]

    def get_region_format(self):
        """省市区"""
        return '{self.province} {self.city} {self.area}'.format(self=self)

    def __str__(self):
        return self.get_region_format() + self.address


class LoginRecord(models.Model):
    """用户的登录历史"""
    user = models.ForeignKey(User)
    username = models.CharField('登录的账号', max_length=64)
    ip = models.CharField('IP', max_length=32)
    address = models.CharField('地址', max_length=32, null=True, blank=True)
    source = models.CharField('登录的来源', max_length=32)

    created_at = models.DateTimeField('登录时间')

    class Meta:
        db_table = 'accounts_login_record'
        verbose_name = '用户登录历史信息'
        verbose_name_plural = '用户登录历史信息'


class PasswdChangeLog(models.Model):
    """用户的密码修改历史"""
    pass
