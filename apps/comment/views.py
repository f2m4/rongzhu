from django.shortcuts import render,redirect
from .forms import MessageForm
from .models import MessagesModel
from django.urls import reverse
# Create your views here.
# 留言板页面
def messages(request):
    context = {}
    # 初始化form的部分数据
    context['messageform'] = MessageForm(initial={'author': request.user.pk})
    messages = MessagesModel.objects.all()
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
        message = MessagesModel()
        message.author = message_form.cleaned_data['author']
        message.title = message_form.cleaned_data['title']
        message.content = message_form.cleaned_data['msg']
        message.save()

    return redirect(referer)