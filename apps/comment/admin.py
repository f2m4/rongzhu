from django.contrib import admin
from .models import MessagesModel
# Register your models here.
@admin.register(MessagesModel)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title', 'content', 'crdate')