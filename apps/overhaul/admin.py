from django.contrib import admin
from . import models


# Register your models here.



@admin.register(models.TaskModel)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'equipment_name', 'content', 'is_get', 'is_complete', 'is_over', 'publisher', 'get_read_num', 'workload',
    'price', 'crdate')


@admin.register(models.DeviceModel)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'under', 'run_is', 'fault_is', 'repair_is', 'remarks', 'crdate')


@admin.register(models.DoTaskModel)
class DoTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'worker', 'task_id', 'crdate')


@admin.register(models.DoTaskEndModel)
class DoTaskEndAdmin(admin.ModelAdmin):
    list_display = ('id', 'dotask_id', 'content', 'remark', 'crdate')
