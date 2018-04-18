from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User

class MessagesModel(models.Model):
    title = models.CharField(max_length=20)
    content = RichTextUploadingField()
    crdate = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    is_del = models.BooleanField(default=False)

    class Meta:
        ordering = ['-crdate']

    def __str__(self):
        return "%s:%s" % (self.author, self.title)