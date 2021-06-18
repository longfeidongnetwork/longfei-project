#!/usr/bin/env python
# _*_ coding:utf-8 _*_
"""
@time: 2021/3/6 14:30
@author:donglongfei
@file: uploadViews.py
"""
from __future__ import unicode_literals

import os
from logging import exception
# Create your views here.
import pymysql
from django.http import JsonResponse

from qualityApp import utils
from qualityApp.utils import mkdir_directory, conversion_size, calculate_duration, update_directory, delete_directory
from quality_inspection.settings import absolute_path


# 查询任务名称
def task_list(request):
    if request.method == 'POST':
        data = request.POST
        name = data.get('name')
        page_num = data.get('pageNum')
        page_num = int(page_num)
        page_size = data.get('pageSize')
        page_size = int(page_size)
        page_count = (page_num - 1) * page_size
        # 使用PyMysql方式查询数据库,使用cursor（）方法获取操作游标
        con = utils.connect_mysql()
        cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            # sql 查询语句
            sql = """select task_id as taskId,task_name as taskName,user_name as userName,
                     DATE_FORMAT(last_time,'%Y-%m-%d %H:%i:%S') lastTime 
                     from task,user as u where task.user_id = u.user_id """
            sql_total = """select count(*) as total from task,user as u where task.user_id = u.user_id """
            if name:
                sql_name = """and task_name like '%%%s%%' """ % name
                sql += sql_name
                sql_total += sql_name
            sql += """order by task.task_id Desc limit %s,%s""" % (page_count, page_size)
            print(sql)
            cursor.execute(sql)
            results = cursor.fetchall()
            print(sql_total)
            cursor.execute(sql_total)
            results_total = cursor.fetchall()

            if not results:
                results = []
            for i in results_total:
                total = i.get('total')
            results = {"content": results, 'total': total}
            result = {'code': 200, 'data': results}
        except Exception as e:
            result = {'code': 400, 'data': str(e)}
        cursor.close()
        con.close()
    else:
        print('请使用post请求！')
    return JsonResponse({'result': result})


# 修改任务名称
def edit_task_name(request):
    if request.method == "POST":
        data = request.POST
        task_id = data.get('taskId')
        task_name = data.get('taskName')
        old_task_name = data.get('oldTaskName')
        update_result = update_directory(old_task_name, task_name)
        if not update_result:
            result = {'code': 400, 'data': '修改目录失败！'}
            return JsonResponse({'result': result})
        # 使用cursor（）方法获取操作游标
        con = utils.connect_mysql()
        cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            # sql 查询语句
            sql = """update task set task_name = '%s' where task_id = '%s' """ % (task_name, task_id)
            print(sql)
            cursor.execute(sql)
            con.commit()
            result = {'code': 200, 'data': "修改成功！"}
        except exception as e:
            con.rollback()
            result = {'code': 400, 'data': str(e)}
    else:
        result = '请使用post请求！'
    return JsonResponse({'result': result})


# 删除任务名称
def delete_task_name(request):
    if request.method == "POST":
        data = request.POST
        task_id = data.get('taskId')
        task_name = data.get('taskName')
        delete_result = delete_directory(task_name)
        if not delete_result:
            result = {'code': 400, 'data': '删除任务失败！'}
            return JsonResponse({'result': result})
        # 使用cursor（）方法获取操作游标
        con = utils.connect_mysql()
        cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            # sql 删除目录下文件
            sql_file = """delete from record where task_id = '%s' """ % task_id
            print(sql_file)
            cursor.execute(sql_file)
            # sql 删除目录语句
            sql = """delete from task  where task_id = '%s' """ % task_id
            print(sql)
            cursor.execute(sql)
            con.commit()
            result = {'code': 200, 'data': "删除成功！"}
        except exception as e:
            con.rollback()
            result = {'code': 400, 'data': str(e)}
    else:
        result = '请使用post请求！'
    return JsonResponse({'result': result})


# 新建任务
def create_task(request):
    if request.method == "POST":
        data = request.POST
        user_id = data.get('userId')
        task_name = data.get('taskName')
        path = absolute_path + task_name
        mkdir_result = mkdir_directory(path)
        if not mkdir_result:
            result = {'code': 400, 'data': '新建失败,目录已存在！'}
            return JsonResponse({'result': result})
        # 使用cursor（）方法获取操作游标
        con = utils.connect_mysql()
        cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            # sql 查询语句
            sql = """insert into task(user_id,task_name,last_time) values ('%s','%s',now())""" % \
                  (user_id, task_name)
            print(sql)
            cursor.execute(sql)
            con.commit()
            result = {'code': 200, 'data': "新增成功！"}
        except exception as e:
            con.rollback()
            result = {'code': 400, 'data': str(e)}
    else:
        result = '请使用post请求！'
    return JsonResponse({'result': result})


# 上传接口
def upload_file(request):
    if request.method == "POST":
        data = request.POST
        task_name = data.get('taskName')
        user_id = data.get('userId')
        obj = request.FILES.get('file')
        # 文件大小
        size = conversion_size(obj.size)
        # 时长
        duration = calculate_duration(obj)
        # 任务id
        task_id = select_task_id(task_name)
        try:
            f = open(os.path.join(absolute_path, task_name, obj.name), 'wb')
            for chunk in obj.chunks():
                f.write(chunk)
            f.close()
            add_audio(task_id, user_id, obj.name, size, duration)
            result = {'code': 200, 'data': "上传成功！"}
        except exception as e:
            result = {'code': 400, 'data': str(e)}
    else:
        result = '请使用post请求！'
    return JsonResponse({'result': result})


# 查询录音详情
def record_list(request):
    if request.method == 'POST':
        data = request.POST
        task_id = data.get('taskId')
        record_name = data.get('recordName')
        page_num = data.get('pageNum')
        page_num = int(page_num)
        page_size = data.get('pageSize')
        page_size = int(page_size)
        page_count = (page_num - 1) * page_size
        # 使用cursor（）方法获取操作游标
        con = utils.connect_mysql()
        cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            # sql 查询语句
            sql = """select record_id as recordId,record_name as recordName,size, duration,
                     DATE_FORMAT(upload_time,'%%Y-%%m-%%d %%H:%%i:%%S') as uploadTime,
                     user_name as uploader from record r left join user u on r.user_id = u.user_id
                     where task_id  = '%s' """ % task_id
            sql_total = """select count(*) as total from record r left join user u 
                           on r.user_id = u.user_id where task_id = '%s' """ % task_id
            if record_name:
                sql_name = """and r.record_name like '%%%s%%' """ % record_name
                sql += sql_name
                sql_total += sql_name
            sql += """order by r.record_id Desc limit %s,%s""" % (page_count, page_size)
            print(sql)
            cursor.execute(sql)
            results = cursor.fetchall()
            print(sql_total)
            cursor.execute(sql_total)
            results_total = cursor.fetchall()
            cursor.close()

            if not results:
                results = []
            for i in results_total:
                total = i.get('total')
            results = {"content": results, 'total': total}
            result = {'code': 200, 'data': results}
        except Exception as e:
            result = {'code': 400, 'data': str(e)}
        con.close()
    else:
        print('请使用post请求！')
    return JsonResponse({'result': result})


# 删除任务名称
def batch_delete_audio(request):
    if request.method == "POST":
        data = request.POST
        record_ids = data.getlist('recordIds')
        task_name = data.get('taskName')
        for id in record_ids:
            record_name = select_record_name(id)
            path = os.path.join(task_name, record_name)
            delete_result = delete_directory(path)
            if not delete_result:
                result = {'code': 400, 'data': '删除任务失败！'}
                return JsonResponse({'result': result})
        # 格式化为字符串
        record_ids = ','.join(record_ids)
        # 使用cursor（）方法获取操作游标
        con = utils.connect_mysql()
        cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            # sql 查询语句
            sql = """delete from record  where record_id in (%s) """ % record_ids
            print(sql)
            cursor.execute(sql)
            con.commit()
            result = {'code': 200, 'data': "删除成功！"}
        except exception as e:
            con.rollback()
            result = {'code': 400, 'data': str(e)}
        cursor.close()
        con.close()
    else:
        result = '请使用post请求！'
    return JsonResponse({'result': result})


# 删除单条录音
def delete_audio(request):
    if request.method == "POST":
        data = request.POST
        record_id = data.get('recordId')
        record_name= data.get('recordName')
        task_name = data.get('taskName')
        path = os.path.join(task_name, record_name)
        delete_result = delete_directory(path)
        if not delete_result:
            result = {'code': 400, 'data': '删除任务失败！'}
            return JsonResponse({'result': result})
        # 使用cursor（）方法获取操作游标
        con = utils.connect_mysql()
        cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            # sql 删除语句
            sql = """delete from record  where record_id = '%s' """ % record_id
            print(sql)
            cursor.execute(sql)
            con.commit()
            result = {'code': 200, 'data': "删除成功！"}
        except exception as e:
            con.rollback()
            result = {'code': 400, 'data': str(e)}
        cursor.close()
        con.close()
    else:
        result = '请使用post请求！'
    return JsonResponse({'result': result})


# 将音频插入数据库
def add_audio(task_id, user_id, name, size, duration):
    # 使用cursor（）方法获取操作游标
    con = utils.connect_mysql()
    cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        # sql 查询语句
        sql = """insert into record(task_id,user_id,record_name,size,duration,upload_time) 
                 values ('%s','%s','%s','%s','%s',now())""" % \
              (task_id, user_id, name, size, duration)
        print(sql)
        cursor.execute(sql)
        con.commit()
        result = {'code': 200, 'data': "新增成功！"}
    except exception as e:
        con.rollback()
        result = {'code': 400, 'data': str(e)}
    cursor.close()
    con.close()
    return JsonResponse({'result': result})


# 根据任务名称查id
def select_task_id(task_name):
    # 使用cursor（）方法获取操作游标
    con = utils.connect_mysql()
    cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        # sql 查询语句
        sql = """select task_id from task where task_name = '%s'""" % task_name
        print(sql)
        cursor.execute(sql)
        result = cursor.fetchone()
        task_id = result["task_id"]
    except exception as e:
        con.rollback()
    cursor.close()
    con.close()
    return task_id


# 根据id查文件名
def select_record_name(id):
    # 使用cursor（）方法获取操作游标
    con = utils.connect_mysql()
    cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        # sql 查询语句
        sql = """select record_name from record where record_id = '%s'""" % id
        print(sql)
        cursor.execute(sql)
        result = cursor.fetchone()
        record_name = result["record_name"]
        print(record_name)
    except exception as e:
        con.rollback()
    cursor.close()
    con.close()
    return record_name

