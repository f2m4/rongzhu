from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from . import models, form
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from countnum.models import ReadnumModel
from django.contrib.contenttypes.models import ContentType
from comment.forms import MessageForm


# Create your views here.
def rongzhu(request):
    return render(request, 'rongzhu/pages/index.html')


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


# 留言板页面
def messages(request):
    context = {}
    # 初始化form的部分数据
    context['messageform'] = MessageForm(initial={'author': request.user.pk})
    messages = models.MessagesModel.objects.all()
    context['messages'] = messages
    context['local'] = True
    return render(request, 'rongzhu/pages/messages.html', context)


# 留言处理
def save_message(request):
    referer = request.META.get('HTTP_REFERER', reverse('rongzhu'))  # 通过反向解析到对应的页面的url
    user = request.user
    # 如果用户未登录.直接返回
    # if not user.is_authenticated:
    #     return redirect(referer)
    # 普通提交,需要验证
    # title = request.POST['title']
    # # 判断内容是否未空  strip() 去除左右空格
    # content = request.POST['msg'].strip()
    # if content == '':
    #     return redirect(referer)
    #
    # try:
    #     pass
    # except Exception as e:
    #     pass
    message_form = MessageForm(request.POST, user=request.user)

    if message_form.is_valid():
        message = models.MessagesModel()
        message.author = message_form.cleaned_data['author']
        message.title = message_form.cleaned_data['title']
        message.content = message_form.cleaned_data['msg']
        message.save()

    return redirect(referer)


# 注销
def logout_go(request):
    logout(request)
    # request.META.get('HTTP_REFERER','/')   #解析到首页,根目录下默认页面的url
    referer = request.META.get('HTTP_REFERER', reverse('rongzhu'))  # 通过反向解析到对应的页面的url
    return redirect(referer)


# 检修任务
def task(request):
    page_num = request.GET.get('page', 1)

    tasks_list = models.TaskModel.objects.filter(is_get=False)
    paginator = Paginator(tasks_list, 5)
    tasks = paginator.page(page_num)
    context = {'tasks': tasks}
    return render(request, 'rongzhu/pages/tasks.html', context)


# 接单页面
def orders(request, task_id):
    context = {}
    # 获取任务,不存在返回404
    task = get_object_or_404(models.TaskModel, pk=task_id)
    ct = ContentType.objects.get_for_model(models.TaskModel)
    # 如果cookies里面不存在阅读标记
    if not request.COOKIES.get('task_%s_num' % task_id):
        if ReadnumModel.objects.filter(object_id=task_id, content_type=ct).count():
            # 存在记录
            readnum = ReadnumModel.objects.get(object_id=task_id, content_type=ct)
        else:
            # 不存在记录
            readnum = ReadnumModel(object_id=task_id, content_type=ct)
        readnum.num += 1
        readnum.save()

    # 上一条记录
    previous_task = models.TaskModel.objects.filter(crdate__gt=task.crdate).last()
    # 吓一跳记录
    next_task = models.TaskModel.objects.filter(crdate__lt=task.crdate).first()
    context['task'] = task
    context['previous_task'] = previous_task
    context['next_task'] = next_task
    respons = render(request, 'rongzhu/pages/orders.html', context)
    respons.set_cookie('task_%s_num' % task_id, True)
    return respons

#工作内容页面
def dotask(request):
    dotask_list=models.DoTaskModel.objects.all()
    dotaskend_list=models.DoTaskEndModel.objects.filter(dotask_id__task_id__is_over=False)
    dotaskendover_list=models.DoTaskEndModel.objects.filter(dotask_id__task_id__is_over=True)
    context={}
    context['dotask_list']=dotask_list
    context['dotaskend_list'] = dotaskend_list
    context['dotaskendover_list'] = dotaskendover_list

    return render(request,'rongzhu/pages/dotasks.html',context)

#接任务
def gettask(request,task_id):
    user=request.user
# 如果用户未登录.直接返回
    if not user.is_authenticated:
        return redirect(reverse('login_in'))
    dotask_add=models.DoTaskModel(worker=user,task_id=models.TaskModel.objects.get(pk=task_id))
    dotask_add.save()
    task_id = models.TaskModel.objects.get(pk=task_id)
    task_id.is_get=True
    task_id.save()
    return redirect(reverse('dotask'))