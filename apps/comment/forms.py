# coding=utf-8
from django import forms
from ckeditor.widgets import CKEditorWidget


class MessageForm(forms.Form):
    title = forms.CharField(label='标题', required=False,max_length=20,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "文章标题"}))
    msg = forms.CharField(label='内容', widget=CKEditorWidget(config_name='message_ckeditor'))
    # 作者是个外键.所以字段是数字
    author = forms.IntegerField(widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        if "user" in kwargs:
            self.user = kwargs.pop('user')
        # 扩展init方法
        super(MessageForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 判断用户是否登录
        if self.user.is_authenticated:
            self.cleaned_data['author']=self.user
        else:
            raise forms.ValidationError('用户未登录')
        return self.cleaned_data
