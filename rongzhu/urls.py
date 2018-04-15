"""rongzhu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings   #导入settings 可以使用里面的定义的变量
from django.conf.urls.static import static   #在开发环境中可以使用这个把media文件加入到url,使其可以被访问到


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('overhaul.urls')),
    path('ckeditor/',include('ckeditor_uploader.urls')),
]
# 设置媒体文件可以被客户端访问到.适用于开发环境.
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)