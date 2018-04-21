from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from . import models, form
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from countnum.models import ReadnumModel
from django.contrib.contenttypes.models import ContentType
from comment.forms import MessageForm
from django.http import JsonResponse


# Create your views here.
def rongzhu(request):
    return render(request, 'rongzhu/pages/index.html')


# 检修任务
def task(request):
    page_num = request.GET.get('page', 1)
    data = {
        'publisher': request.user
    }
    task_form = form.TaskForm(initial=data)
    tasks_list = models.TaskModel.objects.filter(is_get=False)
    paginator = Paginator(tasks_list, 5)
    tasks = paginator.page(page_num)

    current_page = tasks.number  # 获取当前页码
    page_list = list(range(max(current_page - 2, 1), current_page)) + list(
        range(current_page, min(paginator.num_pages, current_page + 2)+1))
    #添加...号
    if page_list[0]-1>=2:
        page_list.insert(0,'...')
    if paginator.num_pages-page_list[-1]>=2:
        page_list.append('...')
    #添加首位页
    if page_list[0]!=1:
        page_list.insert(0,1)
    if page_list[-1]!=paginator.num_pages:
        page_list.append(paginator.num_pages)

    context = {'tasks': tasks, 'task_form': task_form,'page_list':page_list}
    return render(request, 'rongzhu/pages/tasks.html', context)


# 任务添加 ajax
def taskajax(request):
    data = {}

    task = form.TaskForm(request.POST)
    if task.is_valid():
        taskdata = models.TaskModel()
        taskdata.equipment_name = task.cleaned_data['equipment_name']
        taskdata.content = task.cleaned_data['content']
        taskdata.publisher = request.user
        taskdata.workload = task.cleaned_data['workload']
        taskdata.price = task.cleaned_data['price']
        taskdata.save()
        # data['taskdata'] = taskdata
        data['equipment_name'] = taskdata.equipment_name
        data['content'] = taskdata.content
        data['crdate'] = taskdata.crdate.strftime('%Y年%m月%d日 %H:%M:%S')
        data['id'] = taskdata.id
        data['status'] = 'success'
    else:
        data['status'] = 'error'
        #错误信息
        data['message'] = list(task.errors.values())[0][0]
    # return redirect(reverse('task'))
    return JsonResponse(data)


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


# 工作内容页面
def dotask(request):
    dotask_list = models.DoTaskModel.objects.all()
    dotaskend_list = models.DoTaskEndModel.objects.filter(dotask_id__task_id__is_over=False)
    dotaskendover_list = models.DoTaskEndModel.objects.filter(dotask_id__task_id__is_over=True)
    context = {}
    context['dotask_list'] = dotask_list
    context['dotaskend_list'] = dotaskend_list
    context['dotaskendover_list'] = dotaskendover_list

    return render(request, 'rongzhu/pages/dotasks.html', context)


# 接任务
def gettask(request, task_id):
    user = request.user
    # 如果用户未登录.直接返回
    if not user.is_authenticated:
        return redirect(reverse('login_in'))
    #判断用户是否接过该单.一个人只能接一次相同id的单子
    if models.DoTaskModel.objects.filter(worker=user,task_id=models.TaskModel.objects.get(pk=task_id)).count():
        data = {'status': 'error','message':'该任务你已经接单,请勿重复刷新提交.'}
        return JsonResponse(data)
    else:
        dotask_add = models.DoTaskModel(worker=user, task_id=models.TaskModel.objects.get(pk=task_id))
        dotask_add.save()
        task_id = models.TaskModel.objects.get(pk=task_id)
        task_id.is_get = True
        task_id.save()
        # return redirect(reverse('dotask'))
        data={'status':'success'}
        return JsonResponse(data)