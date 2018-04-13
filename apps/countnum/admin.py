from django.contrib import admin
from .models import ReadnumModel
# Register your models here.
@admin.register(ReadnumModel)
class ReadnumAdmin(admin.ModelAdmin):
    list_display = ('num','content_object')