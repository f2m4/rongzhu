# Generated by Django 2.0.3 on 2018-04-14 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('overhaul', '0010_auto_20180414_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskmodel',
            name='content',
            field=models.TextField(),
        ),
    ]
