from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from accounts.forms import UserLoginForm, UserRegistForm


def user_login(request):
    """用户登录"""
    # 第一次访问url get展示表单，供用户输入
    # 第二次访问url post
    if request.method == 'POST':
        form = UserLoginForm(request=request, data=request.POST)
        # client = VerifyCode(request)
        # code = request.POST.get('vcode', None)
        # rest = client.validate_code(code)
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
                return redirect('index')
        else:
            print(form.errors)
    else:
        form = UserLoginForm(request)
    return render(request, 'user_login.html', {
        'form': form
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