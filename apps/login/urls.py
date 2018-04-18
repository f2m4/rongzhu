from django.urls import path
from . import views
urlpatterns=[
    path('login/', views.login_i, name='login'),
    path('out/', views.logout_go, name='logout'),
    path('in/', views.login_form, name='login_in'),
    path('reg/', views.reg, name='reg'),
]