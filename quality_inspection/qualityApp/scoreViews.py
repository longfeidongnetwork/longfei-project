#!/usr/bin/env python
# _*_ coding:utf-8 _*_
"""
@time: 2021/3/7 9:47
@author:donglongfei
@file: scoreViews.py
"""
from __future__ import unicode_literals

import os
from logging import exception
# Create your views here
import pymysql
from django.http import JsonResponse
from qualityApp import scoreSqlMethod, utils, scoreLogicMethod
from qualityApp.scoreLogicMethod import get_keyword_time
from qualityApp.scoreSqlMethod import select_record_id, select_rating_details, update_rating_details, get_lrc, \
    get_record, select_task_name, query_record_name
from quality_inspection.settings import lrc_path


# 查询评分目录
def directory_list(request):
    if request.method == 'POST':
        data = request.POST
        task_name = data.get('taskName')
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
            sql = """select distinct task_id as taskId, task_name as taskName, 
                    (select count(1) from record r where r.task_id = t.task_id) as audioCount,
                    DATE_FORMAT(last_time,'%Y-%m-%d %H:%i:%S') lastTime  
                    from task t where 1=1 """
            sql_total = """select count(*) as total from task t,user u where t.user_id = u.user_id """
            if task_name:
                sql_name = """and t.task_name like '%%%s%%' """ % task_name
                sql += sql_name
                sql_total += sql_name
            sql += """order by t.task_id Desc limit %s,%s""" % (page_count, page_size)
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
            print(e)
            result = {'code': 400, 'data': str(e)}
        con.close()
    else:
        print('请使用post请求！')
    return JsonResponse({'result': result})


# 更改目录名称
def update_directory_name(request):
    if request.method == "POST":
        data = request.POST
        task_id = data.get('taskId')
        task_name = data.get('taskName')
        # 使用PyMysql方式查询数据库,使用cursor（）方法获取操作游标
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
        cursor.close()
        con.close()
    else:
        result = '请使用post请求！'
    return JsonResponse({'result': result})


# 删除目录名称
def delete_directory_name(request):
    if request.method == "POST":
        data = request.POST
        task_id = data.get('taskId')
        # 使用PyMysql方式查询数据库,使用cursor（）方法获取操作游标
        con = utils.connect_mysql()
        cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            # sql 查询语句
            sql = """delete from task  where task_id = '%s' """ % task_id
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


# 质检
def quality_inspection(request):
    """
    对选中的任务名称进行质检
    :param request: planId:方案 taskIds:任务名称(支持多选)
    :return:
    """
    if request.method == "POST":
        data = request.POST
        plan_id = data.get("planId")
        task_ids = data.getlist("taskIds")
        record_ids = data.getlist("params")
        try:
            # 选中具体录音返回lrc文件
            if record_ids:
                lrc_list = scoreSqlMethod.select_record_ids(task_ids, record_ids)
            else:
                # 查找所有的目录名下所有lrc文件
                lrc_list = scoreSqlMethod.select_task_ids(task_ids)
            if lrc_list:
                # 对lrc文件进行质检
                result = scoreLogicMethod.quality_lrc(lrc_list, plan_id)
                if result:
                    result = {'code': 200, 'data': "质检成功！"}
                else:
                    result = {'code': 400, 'data': "质检失败！"}
            else:
                result = {'code': 400, 'data': "没有找到质检文件！"}
        except exception as e:
            result = {'code': 400, 'data': str(e)}
    else:
        result = '请使用post请求！'
    return JsonResponse({'result': result})


# 质检结果列表
def result_list(request):
    if request.method == 'POST':
        data = request.POST
        task_id = data.get('taskId')
        record_name = data.get('recordName')
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
            sql = """  SELECT result.result_id as resultId,r.task_id as taskId,r.record_id as recordId,r.record_name as 
                       recordName,p.plan_id as planId,p.plan_name as planName,result.key1 as key1,result.key2 as key2,
                       result.key3 as key3, result.score as score 
                       FROM result LEFT JOIN record r ON result.record_id = r.record_id 
                       LEFT JOIN plan p ON result.plan_id = p.plan_id
                       LEFT JOIN task t ON r.task_id = t.task_id where r.task_id = '%s'""" % task_id
            sql_total = """  SELECT count(*) as total
                                   FROM result LEFT JOIN record r ON result.record_id = r.record_id 
                                   LEFT JOIN plan p ON result.plan_id = p.plan_id
                                   LEFT JOIN task t ON r.task_id = t.task_id where r.task_id = '%s' """ % task_id
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
            print(e)
            result = {'code': 400, 'data': str(e)}
        con.close()
    else:
        print('请使用post请求！')
    return JsonResponse({'result': result})


# 删除质检结果
def delete_result(request):
    if request.method == "POST":
        data = request.POST
        task_id = data.get('taskId')
        result_id = data.get('resultId')
        # 根据result_id 查询record_id
        record_id = select_record_id(result_id)
        record_name = query_record_name(record_id)
        portion = os.path.splitext(record_name)
        lrc_name = portion[0] + '.lrc'
        # 根据task_id 查询 task_name
        task_name = select_task_name(task_id)
        # 使用PyMysql方式查询数据库,使用cursor（）方法获取操作游标
        con = utils.connect_mysql()
        cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            # sql 删除语句
            sql_result = """delete from result  where result_id = '%s' """ % result_id
            sql_record = """delete from record where record_id = '%s' """ % record_id
            cursor.execute(sql_result)
            cursor.execute(sql_record)
            con.commit()
            file_path = os.path.join(lrc_path, task_name, lrc_name)
            if os.path.exists(file_path):
                os.remove(file_path)
            result = {'code': 200, 'data': "删除成功！"}
        except exception as e:
            con.rollback()
            result = {'code': 400, 'data': str(e)}
        cursor.close()
        con.close()
    else:
        result = '请使用post请求！'
    return JsonResponse({'result': result})


# 上一条录音
def last_result(request):
    if request.method == "POST":
        data = request.POST
        record_id = data.get("recordId")
        task_id = data.get("taskId")
        # 使用PyMysql方式查询数据库,使用cursor（）方法获取操作游标
        con = utils.connect_mysql()
        cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            # 查询语句
            sql = """select r.record_id as recordId,r.record_name recordName from record r join task t on 
                     r.task_id = t.task_id where t.task_id = '%s' and r.record_id=(select min(r.record_id) 
                     from record r where r.record_id > '%s' and task_id = '%s');""" % (task_id, record_id, task_id)
            print(sql)
            cursor.execute(sql)
            results = cursor.fetchone()
            cursor.close()
            if results:
                results = {'content': results}
                result = {'code': 200, 'data': results}
            else:
                result = {'code': 201, 'data': "已到最新数据！"}
        except exception as e:
            result = {'code': 400, 'data': str(e)}
        con.close()
    else:
        print("请使用post请求！")
    return JsonResponse({'result': result})


# 下一条录音
def next_result(request):
    if request.method == "POST":
        data = request.POST
        record_id = data.get("recordId")
        task_id = data.get("taskId")
        # 使用PyMysql方式查询数据库,使用cursor（）方法获取操作游标
        con = utils.connect_mysql()
        cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            # 查询语句
            sql = """select r.record_id as recordId,r.record_name recordName from record r join task t on 
                     r.task_id = t.task_id where t.task_id = '%s' and r.record_id=(select max(r.record_id) 
                     from record r where r.record_id < '%s' and task_id = '%s');""" % (task_id, record_id, task_id)
            print(sql)
            cursor.execute(sql)
            results = cursor.fetchone()
            cursor.close()
            if results:
                results = {'content': results}
                result = {'code': 200, 'data': results}
            else:
                result = {'code': 201, 'data': "已到最新数据！"}
        except exception as e:
            result = {'code': 400, 'data': str(e)}
        con.close()
    else:
        print("请使用post请求！")
    return JsonResponse({'result': result})


# 评分详情展示
def detail_result(request):
    """
    打分详情
    :param request:
    :return:
    """
    if request.method == "POST":
        data = request.POST
        try:
            record_id = data.get("recordId")
            results, plan_name, score = select_rating_details(record_id)
            if results:
                results = {'content': results, 'planName': plan_name, 'score': score}
                result = {'code': 200, 'data': results}
            else:
                results = {'content': results, 'planName': plan_name, 'score': score}
                result = {'code': 201, 'data': results}
        except exception as e:
            result = {'code': 400, 'data': str(e)}
    else:
        print("请使用post请求！")
    return JsonResponse({'result': result})


# 人工打分
def edit_result(request):
    """
    人工打分
    :param request:
    :return:
    """
    if request.method == "POST":
        data = request.POST
        try:
            record_id = data.get("recordId")
            score = data.get("score")
            series = data.get("series")
            results = update_rating_details(record_id, score, series)
            if results:
                result = {'code': 200, 'data': "人工打分成功！"}
            else:
                result = {'code': 400, 'data': "人工打分失败！"}
        except exception as e:
            result = {'code': 400, 'data': str(e)}
    else:
        print("请使用post请求！")
    return JsonResponse({'result': result})


# 获取lrc文件
def get_lrc_file(request):
    """
    获取lrc文件
    :param request:
    :return:
    """
    if request.method == "POST":
        data = request.POST
        record_id = data.get("recordId")
        task_id = data.get("taskId")
        lrc_file = get_lrc(record_id, task_id)
        print(lrc_file)
        if lrc_file:
            results = {'lrcFile': lrc_file}
            result = {'code': 200, 'data': results}
        else:
            result = {'code': 400, 'data': "人工打分失败！"}
    else:
        print("请使用post请求！")
    return JsonResponse({'result': result})


# 获取音频文件
def get_record_file(request):
    """
    获取音频文件
    :param request:
    :return:
    """
    if request.method == "POST":
        data = request.POST
        record_id = data.get("recordId")
        task_id = data.get("taskId")
        record_file = get_record(record_id, task_id)
        print(record_file)
        if record_file:
            results = {'recordFile': record_file}
            result = {'code': 200, 'data': results}
        else:
            result = {'code': 400, 'data': "人工打分失败！"}
    else:
        print("请使用post请求！")
    return JsonResponse({'result': result})


# 关键词时间对应关系查询
def keyword_time_result(request):
    """
    查询关键词时间
    :param request:
    :return:
    """
    if request.method == "POST":
        data = request.POST
        keyword = data.get("keyword")
        record_id = data.get("recordId")
        record_name = query_record_name(record_id)
        portion = os.path.splitext(record_name)
        csv_name = portion[0] + '.csv'
        keyword_time = get_keyword_time(keyword, csv_name)
        print(keyword_time)
        results = {'keywordTime': keyword_time}
        result = {'code': 200, 'data': results}
    else:
        print("请使用post请求！")
    return JsonResponse({'result': result})


