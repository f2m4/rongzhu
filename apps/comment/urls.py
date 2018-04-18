from django.urls import path
from . import views
urlpatterns = [
    path('index/', views.messages, name='messages'),
    path('save_message/', views.save_message, name='save_message'),
]
