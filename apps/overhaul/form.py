from django import forms
from django.contrib.auth.models import User
from django.contrib import auth
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from ckeditor_uploader.fields import RichTextUploadingFormField
from ckeditor.fields import RichTextFormField

class LoginForm(forms.Form):
    username=forms.CharField(min_length=4,label='用户名',widget=forms.TextInput(attrs={'class':'form-control','placeholder':"用户名"}))
    password=forms.CharField(label='密码',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':"密码"}))
    def clean(self):
        username=self.cleaned_data['username']
        password=self.cleaned_data['password']
        #验证用户名,密码是否匹配,不匹配返回none.
        user=auth.authenticate(username=username,password=password)
        if user is None:
            raise forms.ValidationError('用户名或密码错误!!')
        else:
            self.cleaned_data['user']=user
        return self.cleaned_data

class RegForm(forms.Form):
    username=forms.CharField(min_length=4,max_length=20,label='用户名',widget=forms.TextInput(attrs={'class':'form-control','placeholder':"4-20位用户名"}))
    email=forms.EmailField(label='邮箱',widget=forms.EmailInput(attrs={'class':'form-control','placeholder':"有效邮箱"}))
    password=forms.CharField(min_length=8,label='密码',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':"至少8位"}))
    password_again=forms.CharField(min_length=8,label='密码',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':"确认密码"}))
    def clean_username(self):
        username=self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("用户已存在")
        return username
    def clean_email(self):
        email=self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("email已存在")
        return email
    def clean_password_again(self):
        password=self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError("两次密码输入不一致!")
        return password_again

class TaskForm(forms.Form):
    equipment_name=forms.CharField(label='设备名称',max_length=50,widget=forms.TextInput(attrs={'class':'form-control','placeholder':"维修部位"}))
    content = forms.CharField(label='故障原因',widget=CKEditorUploadingWidget(config_name='task_ckeditor'))
    workload=forms.IntegerField(label='工时',widget=forms.NumberInput(attrs={'class':'form-control','placeholder':"工时"}))
    price=forms.IntegerField(label='价格(元)',widget=forms.NumberInput(attrs={'class':'form-control','placeholder':"价格"}))
    publisher=forms.CharField(label='发布人',widget=forms.HiddenInput())
