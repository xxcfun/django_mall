import re

from django import forms
from django.contrib.auth import authenticate, login

from django.contrib.auth.models import User
from django.http import request

from utils.verify import VerifyCode


class UserLoginForm(forms.Form):
    """用户登录表单"""
    username = forms.CharField(label='用户名', max_length=64)
    password = forms.CharField(label='密码', max_length=64,
                               widget=forms.PasswordInput,
                               error_messages={
                                   'required': '请输入密码'
                               })
    verify_code = forms.CharField(label='验证码', max_length=4,
                                  error_messages={
                                      'required': '请输入验证码'
                                  })

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    # def clean_username(self):
    #     """验证用户名hook钩子函数"""
    #     username = self.cleaned_data['username']
    #     # print(username)
    #     # 判断用户名是否为手机号码
    #     pattern = r'^1[0-9]{10}$'
    #     if not re.search(pattern, username):
    #         raise forms.ValidationError('请输入正确的手机号')
    #     return username

    def clean_verify_code(self):
        """验证用户输入的验证码是否正确"""
        verify_code = self.cleaned_data['verify_code']
        if not verify_code:
            raise forms.ValidationError('请输入验证码')
        client = VerifyCode(self.request)
        if not client.validate_code(verify_code):
            raise forms.ValidationError('您输入的验证码不正确')
        return verify_code

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get('username', None)
        password = cleaned_data.get('password', None)
        if username and password:
            # 查询用户名和密码匹配的用户
            user_list = User.objects.filter(username=username)
            if user_list.count() == 0:
                raise forms.ValidationError('用户名不存在')
            # 验证密码是否正确
            # if not user_list.filter(password=password).exists():
            #     raise forms.ValidationError('密码错误')
            if not authenticate(username=username, password=password):
                raise forms.ValidationError('密码错误')
        return cleaned_data


class UserRegistForm(forms.Form):
    """用户注册表单"""
    username = forms.CharField(label='用户名', max_length=64)
    # nickname = forms.CharField(label='昵称', max_length=64)
    password = forms.CharField(label='密码', max_length=64, widget=forms.PasswordInput)
    password_repeat = forms.CharField(label='重复密码', max_length=64, widget=forms.PasswordInput)
    verify_code = forms.CharField(label='验证码', max_length=4)

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_username(self):
        """验证用户名是否已经被注册"""
        data = self.cleaned_data['username']
        if User.objects.filter(username=data).exists():
            raise forms.ValidationError('用户名已存在')
        return data

    def clean_verify_code(self):
        """验证输入验证码是否有误"""
        verify_code = self.cleaned_data['verify_code']
        if not verify_code:
            raise forms.ValidationError('请输入验证码')
        client = VerifyCode(self.request)
        if not client.validate_code(verify_code):
            raise forms.ValidationError('您输入的验证码不正确')
        return verify_code

    def clean(self):
        """验证密码"""
        cleaned_data = super().clean()
        password = cleaned_data.get('password', None)
        password_repeat = cleaned_data.get('password_repeat', None)
        if password and password_repeat:
            if password != password_repeat:
                raise forms.ValidationError('两次密码输入不一致')
        return cleaned_data

    def register(self):
        """注册方法"""
        data = self.cleaned_data
        # 1.创建用户
        User.objects.create_user(username=data['username'],
                                 password=data['password'])
        # 2.自动登录
        user = authenticate(username=data['username'],
                            password=data['password'])
        login(self.request, user)
        return user


class UserForm(forms.ModelForm):
    pass
    """从模型创建表单"""
    #
    # class Meta:
    #     model = User
    #     fields = ['username', 'password']
    #     # 界面表单数据修改
    #     widgets = {
    #         'password': forms.PasswordInput(attrs={
    #             'class': 'text-error'
    #         })
    #     }
    #     labels = {
    #         'username': '手机号码'
    #     }
    #     error_messages = {
    #         'username': {
    #             'required': '请输入手机号码',
    #             'max_length': '最长不超过32位'
    #         }
    #     }
