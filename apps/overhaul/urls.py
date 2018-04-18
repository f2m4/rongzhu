from django.urls import path
from . import views

urlpatterns = [
    path('', views.rongzhu, name='rongzhu'),
    path('task/', views.task, name='task'),
    path('orders/<int:task_id>', views.orders, name='orders'),
    path('dotask/',views.dotask,name='dotask'),
    path('gettask/<int:task_id>',views.gettask,name='gettask'),
    path('task/add',views.taskajax,name='taskajax'),
]
