from django.shortcuts import render,redirect
from . import form
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
# Create your views here.

# 登录,通过modal登录.
def login_i(request):
    username = request.POST['name']
    password = request.POST['password']
    # request.META.get('HTTP_REFERER','/')   #解析到首页,根目录下默认页面的url
    referer = request.META.get('HTTP_REFERER', reverse('rongzhu'))  # 通过反向解析到对应的页面的url
    # 验证用户名和密码
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # 返回到指定页面
        return redirect(referer)
    else:
        login_f = form.LoginForm()
        context = {}
        context['login_f'] = login_f
        context['error'] = "用户名或密码错误!"
        return render(request, 'rongzhu/pages/error_login.html', context)
        # return redirect(reverse('login_in'))#从定向到登录页面,可错误提示不好弄.


# 通过自带的form来设计登录
def login_form(request):
    if request.method == "POST":
        login_f = form.LoginForm(request.POST)
        if login_f.is_valid():
            user = login_f.cleaned_data['user']
            login(request, user)
            return redirect(request.GET.get('from', reverse('rongzhu')))
    else:
        login_f = form.LoginForm()
    context = {}
    context['login_f'] = login_f
    return render(request, 'rongzhu/pages/login.html', context)


# 通过form设计的注册
def reg(request):
    if request.method == "POST":
        reg_form = form.RegForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            user = User.objects.create_user(username, email, password)
            user.save()
            # 登录
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect(request.GET.get('from', reverse('rongzhu')))

    else:
        reg_form = form.RegForm()
    context = {"reg_form": reg_form}
    return render(request, 'rongzhu/pages/reg.html', context)





# 注销
def logout_go(request):
    logout(request)
    # request.META.get('HTTP_REFERER','/')   #解析到首页,根目录下默认页面的url
    referer = request.META.get('HTTP_REFERER', reverse('rongzhu'))  # 通过反向解析到对应的页面的url
    return redirect(referer)