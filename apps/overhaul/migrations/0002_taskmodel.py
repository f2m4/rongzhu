# Generated by Django 2.0.3 on 2018-04-07 15:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('overhaul', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('equipment_name', models.CharField(max_length=50)),
                ('content', models.TextField()),
                ('crdate', models.DateTimeField(auto_now_add=True)),
                ('complete', models.BooleanField(default=False)),
                ('workload', models.IntegerField(default=1)),
                ('price', models.IntegerField(default=10)),
                ('publisher', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-crdate'],
            },
        ),
    ]
