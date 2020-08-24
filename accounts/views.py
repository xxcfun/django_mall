from django.shortcuts import render

# Create your views here.
from accounts.forms import UserLoginForm, UserRegistForm


def user_login(request):
    """用户登录"""
    # 第一次访问url get展示表单，供用户输入
    # 第二次访问url post
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        # 表单是否通过了验证
        if form.is_valid():
            # 执行
            pass
        else:
            print(form.errors)
    else:
        form = UserLoginForm
    return render(request, 'user_login.html', {
        'form': form
    })


def user_register(request):
    """用户注册"""
    form = UserRegistForm()
    return render(request, 'user_register.html', {
        'form': form
    })