# Generated by Django 2.0.3 on 2018-04-12 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('overhaul', '0008_auto_20180412_1510'),
    ]

    operations = [
        migrations.RenameField(
            model_name='taskmodel',
            old_name='complete',
            new_name='is_complete',
        ),
        migrations.RemoveField(
            model_name='dotaskendmodel',
            name='is_over',
        ),
        migrations.AddField(
            model_name='taskmodel',
            name='is_get',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='taskmodel',
            name='is_over',
            field=models.BooleanField(default=False),
        ),
    ]
