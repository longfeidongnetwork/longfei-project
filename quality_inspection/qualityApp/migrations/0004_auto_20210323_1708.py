# Generated by Django 3.1.4 on 2021-03-23 17:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qualityApp', '0003_auto_20210323_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='last_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 23, 17, 8, 3, 399014), verbose_name='修改日期'),
        ),
        migrations.AlterField(
            model_name='record',
            name='extension_name',
            field=models.CharField(default='null', max_length=5),
        ),
        migrations.AlterField(
            model_name='record',
            name='upload_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 23, 17, 8, 3, 399014), verbose_name='上传日期'),
        ),
        migrations.AlterField(
            model_name='result',
            name='inspection_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 23, 17, 8, 3, 399014), verbose_name='质检日期'),
        ),
        migrations.AlterField(
            model_name='task',
            name='last_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 23, 17, 8, 3, 400010), verbose_name='新建日期'),
        ),
    ]