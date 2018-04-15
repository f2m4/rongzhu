from django.db import models
from django.contrib.auth.models import User
from countnum.models import ReadnumModel, ReadnumExnum
from ckeditor_uploader.fields import RichTextUploadingField

class DeviceModel(models.Model):
    name = models.CharField(max_length=30)
    crdate = models.DateTimeField(auto_now_add=True)
    # 是否在运行 默认 运行
    run_is = models.BooleanField(default=True)
    # 是否存在故障 默认 不存在
    fault_is = models.BooleanField(default=False)
    # 所属生产线
    under = models.CharField(max_length=20)
    # 其他备注信息
    remarks = models.TextField(blank=True)
    # 是否在修理中 默认 不在修
    repair_is = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# Create your models here.
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


# class AltpyeModel(models.Model):
#     name=models.CharField(max_length=10)
#     alin=models.DecimalField()
#     mgin=models.DecimalField()
#     siin=models.DecimalField()
#     fein=models.DecimalField()
#     mnin=models.DecimalField()
#     cuin=models.DecimalField()
#     def __str__(self):
#         return self.name
#     class Meta:
#         ordering=['name']
class TaskModel(models.Model, ReadnumExnum):
    # 设备名称
    equipment_name = models.CharField(max_length=50)
    content = RichTextUploadingField()
    crdate = models.DateTimeField(auto_now_add=True)
    # 是否接单
    is_get = models.BooleanField(default=False)
    # 接单是否完成
    is_complete = models.BooleanField(default=False)
    # 是否审核结束
    is_over=models.BooleanField(default=False)
    # 发布者
    publisher = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    # 工时
    workload = models.IntegerField(default=1)
    # 价格
    price = models.IntegerField(default=10)

    class Meta:
        ordering = ['-crdate']

    def __str__(self):
        return self.equipment_name


class DoTaskModel(models.Model):
    # 接单人
    worker = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    crdate = models.DateTimeField(auto_now_add=True)
    task_id = models.ForeignKey(TaskModel, on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ['-crdate']

    def __str__(self):
        return '%s task is repair by %s' % (self.task_id, self.worker)


class DoTaskEndModel(models.Model):
    dotask_id = models.ForeignKey(DoTaskModel, on_delete=models.DO_NOTHING)
    # 工作内容
    content = models.TextField()
    crdate = models.DateTimeField(auto_now_add=True)
    # 备注
    remark = models.TextField(blank=True)

    class Meta:
        ordering = ['-crdate']

    def __str__(self):
        return '%s task for %s' % (self.dotask_id.task_id, self.dotask_id)
