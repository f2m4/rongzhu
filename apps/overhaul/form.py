from django import forms
from django.contrib.auth.models import User
from django.contrib import auth
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from ckeditor_uploader.fields import RichTextUploadingFormField
from ckeditor.fields import RichTextFormField



class TaskForm(forms.Form):
    equipment_name=forms.CharField(label='设备名称',max_length=50,widget=forms.TextInput(attrs={'class':'form-control','placeholder':"维修部位"}))
    content = forms.CharField(label='故障原因',widget=CKEditorUploadingWidget(config_name='task_ckeditor'),error_messages={'required':'故障原因不能为空!'})
    workload=forms.IntegerField(label='工时',widget=forms.NumberInput(attrs={'class':'form-control','placeholder':"工时"}))
    price=forms.IntegerField(label='价格(元)',widget=forms.NumberInput(attrs={'class':'form-control','placeholder':"价格"}))
    publisher=forms.CharField(label='发布人',widget=forms.HiddenInput())
    def clean(self):
        return self.cleaned_data