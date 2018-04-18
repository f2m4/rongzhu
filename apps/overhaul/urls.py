from django.urls import path
from . import views

urlpatterns = [
    path('', views.rongzhu, name='rongzhu'),
    path('login/', views.login_i, name='login'),
    path('logout_go/', views.logout_go, name='logout'),
    path('login_in/', views.login_form, name='login_in'),
    path('reg/', views.reg, name='reg'),
    path('task/', views.task, name='task'),
    path('orders/<int:task_id>', views.orders, name='orders'),
    path('dotask/',views.dotask,name='dotask'),
    path('gettask/<int:task_id>',views.gettask,name='gettask'),
]
