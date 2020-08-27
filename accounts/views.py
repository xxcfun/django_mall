from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from accounts.forms import UserLoginForm, UserRegistForm, UserAddressForm
from accounts.models import UserAddress
from utils.verify import VerifyCode


def user_login(request):
    """用户登录"""
    # 如果登录是从其他页面跳转过来的，会带next参数，如果有next参数，登录完成后，
    # 需要跳转到next所对应的地址，否则，跳转到首页上去
    next_url = request.GET.get('next', 'index')
    # 第一次访问url get展示表单，供用户输入
    # 第二次访问url post
    if request.method == 'POST':
        form = UserLoginForm(request=request, data=request.POST)
        client = VerifyCode(request)
        code = request.POST.get('vcode', None)
        rest = client.validate_code(code)
        # 表单是否通过了验证
        if form.is_valid():
            # 执行登录
            data = form.cleaned_data
            # # 查询用户信息
            # user = User.objects.get(username=data['username'], password=data['password'])
            # # 设置用户ID到session
            # request.session[constants.LOGIN_SESSION_ID] = user.id
            # # 登录后的跳转
            # return redirect('index')

            # 使用自定义方法进行登录
            # 使用django-auth来实现登录
            user = authenticate(request, username=data['username'], password=data['password'])
            if user is not None:
                login(request, user)
                # 登录后的跳转

                return redirect(next_url)
        else:
            print(form.errors)
    else:
        form = UserLoginForm(request)
    return render(request, 'user_login.html', {
        'form': form,
        'next_url': next_url
    })


def user_logout(request):
    """用户退出登录"""
    logout(request)
    return redirect('index')


def user_register(request):
    """用户注册"""
    if request.method == 'POST':
        form = UserRegistForm(request=request, data=request.POST)
        if form.is_valid():
            # 调用注册方法
            form.register()
            return redirect('index')
        else:
            print(form.errors)
    else:
        form = UserRegistForm(request=request)
    return render(request, 'user_register.html', {
        'form': form
    })


@login_required
def address_list(request):
    """地址列表"""
    my_addr_list = UserAddress.objects.filter(user=request.user, is_valid=True)
    return render(request, 'address_list.html', {
        'my_addr_list': my_addr_list
    })


@login_required()
def address_edit(request, pk):
    """地址新增或者是编辑"""
    addr = None
    initial = {}
    # 如果pk是数字，则表示修改
    if pk.isdigit():  # isdigit() 检测字符串是否只有数字组成
        addr = get_object_or_404(UserAddress, pk=pk, user=request.user, is_valid=True)
        initial['region'] = addr.get_region_format()
    if request.method == 'POST':
        form = UserAddressForm(request=request, data=request.POST, initial=initial, instance=addr)
        if form.is_valid():
            form.save()
            return redirect('accounts:address_list')
    else:
        form = UserAddressForm(request=request, instance=addr, initial=initial)
    return render(request, 'address_edit.html', {
        'form': form
    })


def address_delete(request, pk):
    """删除地址"""
    addr = get_object_or_404(UserAddress, pk=pk, user=request.user, is_valid=True)
    addr.is_valid = False
    addr.save()
    return HttpResponse('ok')
