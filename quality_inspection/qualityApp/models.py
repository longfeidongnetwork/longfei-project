from __future__ import unicode_literals
from django.db import models


# Create your models here.
from django.utils import timezone


class keyword(models.Model):
    keyword_id = models.AutoField(primary_key=True)
    series_id = models.IntegerField(max_length=11)
    key_word = models.CharField(max_length=20)
    homophonic_word = models.CharField(max_length=100)
    related_word = models.CharField(max_length=20)
    second = models.SmallIntegerField(max_length=6)

    class Meta:
        db_table = "keyword"


class plan(models.Model):
    plan_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(max_length=11)
    plan_name = models.CharField(max_length=20)
    total_score = models.SmallIntegerField(max_length=6)
    last_time = models.DateTimeField('修改日期', default=timezone.now())

    class Meta:
        db_table = "plan"


class record(models.Model):
    record_id = models.AutoField(primary_key=True)
    task_id = models.IntegerField(max_length=11)
    user_id = models.IntegerField(max_length=11)
    record_name = models.CharField(max_length=50)
    extension_name = models.CharField(max_length=5, null=True)
    size = models.CharField(max_length=10)
    duration = models.SmallIntegerField(max_length=6)
    upload_time = models.DateTimeField('上传日期', default=timezone.now())
    extension_number = models.IntegerField(max_length=11, null=True)

    class Meta:
        db_table = "record"


class result(models.Model):
    result_id = models.AutoField(primary_key=True)
    record_id = models.IntegerField(max_length=11)
    plan_id = models.IntegerField(max_length=11)
    user_id = models.IntegerField(max_length=11)
    inspection_time = models.DateTimeField('质检日期', default=timezone.now())
    score = models.SmallIntegerField(max_length=11)
    key1 = models.CharField(max_length=20)
    key2 = models.CharField(max_length=20)
    key3 = models.CharField(max_length=20)
    rating_details = models.CharField(max_length=252)
    series_keyword = models.TextField(null=True)

    class Meta:
        db_table = "result"


class role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=20)
    role_level = models.SmallIntegerField(max_length=6)

    class Meta:
        db_table = "role"


class series(models.Model):
    series_id = models.AutoField(primary_key=True)
    plan_id = models.CharField(max_length=20)
    series_name = models.CharField(max_length=20)
    series_type = models.IntegerField(max_length=11)
    series_score = models.SmallIntegerField(max_length=6)
    everyhit_score = models.SmallIntegerField(max_length=6)
    frequency = models.SmallIntegerField(max_length=6)

    class Meta:
        db_table = "series"


class task(models.Model):
    task_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(max_length=11)
    task_name = models.CharField(max_length=20)
    last_time = models.DateTimeField('新建日期', default=timezone.now())

    class Meta:
        db_table = "task"


class user(models.Model):
    user_id = models.AutoField(primary_key=True)
    role_id = models.IntegerField(max_length=11, null=True)
    user_name = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    parent_id = models.IntegerField(max_length=11, null=True)
    mark = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = "user"


class customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=11)
    extension_number = models.IntegerField(max_length=11, null=True)

    class Meta:
        db_table = "customer"
