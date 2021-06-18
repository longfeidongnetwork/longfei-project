#!/usr/bin/env python
# _*_ coding:utf-8 _*_
"""
@time: 2021/3/8 12:49
@author:donglongfei
@file: planViews.py
"""
from __future__ import unicode_literals

import os
from logging import exception
import pymysql
from django.http import JsonResponse

from qualityApp import utils
from qualityApp.planSqlMethod import plan_total_score
from quality_inspection.settings import absolute_path, series_path


# 查询方案列表
def plan_list(request):
    if request.method == 'POST':
        data = request.POST
        # 参数获取
        plan_name = data.get('planName')
        page_num = data.get('pageNum')
        page_num = int(page_num)
        page_size = data.get('pageSize')
        page_size = int(page_size)
        page_count = (page_num -1) * page_size
        # 使用PyMysql方式查询数据库,使用cursor（）方法获取操作游标
        con = utils.connect_mysql()
        cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            # sql语句
            sql = """select plan_id as planId,user_id as userId,plan_name as planName,total_score as totalScore,
                     DATE_FORMAT(last_time,'%Y-%m-%d %H:%i:%S') lastTime  from plan p where 1=1 """
            sql_total = """select count(*) as total from plan p where 1=1 """
            if plan_name:
                sql_name = """and p.plan_name like '%%%s%%' """ % plan_name
                sql += sql_name
                sql_total += sql_name
            sql += """order by p.plan_id asc limit %s,%s""" % (page_count, page_size)
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


# 方案修改
def edit_plan(request):
    if request.method == "POST":
        data = request.POST
        plan_id = data.get('planId')
        plan_name = data.get('planName')
        # 使用PyMysql方式查询数据库,使用cursor（）方法获取操作游标
        con = utils.connect_mysql()
        cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            # sql修改语句
            sql = """update plan set plan_name = '%s' where plan_id = '%s'""" %(plan_name, plan_id)
            print(sql)
            cursor.execute(sql)
            con.commit()
            result = {'code': 200, 'data': '修改成功'}
        except exception as e:
            con.rollback()
            result = {'code': 400, 'data': str(e)}
        cursor.close()
        con.close()
    else:
        result = {'code': 400, 'data': '请使用post请求！'}
    return JsonResponse({'result': result})


# 方案选择器
def plan_select(request):
    if request.method == 'POST':
        data = request.POST
        # 使用PyMysql方式查询数据库,使用cursor（）方法获取操作游标
        con = utils.connect_mysql()
        cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            # sql语句
            sql = """select plan_id as planId,plan_name as planName from plan """
            print(sql)
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            print(results)
            results = {"content": results}
            result = {'code': 200, 'data': results}
        except Exception as e:
            print(e)
            result = {'code': 400, 'data': str(e)}
        con.close()
    else:
        print('请使用post请求！')
    return JsonResponse({'result': result})


# 搜索组别
def series_list(request):
    if request.method == 'POST':
        data = request.POST
        plan_id = data.get("planId")
        series_type = data.get("statisticalValue")
        page_num = data.get('pageNum')
        page_num = int(page_num)
        page_size = data.get('pageSize')
        page_size = int(page_size)
        page_count = (page_num - 1) * page_size
        # 使用PyMysql方式查询数据库,使用cursor（）方法获取操作游标
        con = utils.connect_mysql()
        cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            sql = """select series_id as seriesId,plan_id as planId, series_name as seriesName,
                     series_score as seriesScore, everyhit_score as everyHitScore, frequency
                     from series where plan_id = '%s' and series_type = '%s'""" % (plan_id, series_type)
            sql_total = """select count(*) as total from series 
                     where plan_id='%s'and series_type = '%s'""" % (plan_id, series_type)
            sql += """order by series.series_id desc limit %s,%s""" % (page_count, page_size)
            print(sql)
            cursor.execute(sql)
            results = cursor.fetchall()
            print(sql_total)
            cursor.execute(sql_total)
            result_total = cursor.fetchall()
            cursor.close()
            if not results:
                results = []
            for i in result_total:
                total = i.get('total')
            results = {"content": results, 'total': total}
            result = {'code': 200, 'data': results}
        except exception as e:
            result = {'code': 400, 'data': str(e)}
        cursor.close()
        con.close()
    else:
        print('请使用post请求！')
    return JsonResponse({'result': result})


# 新增组别
def create_series(request):
    if request.method == "POST":
        data = request.POST
        plan_id = data.get('planId')
        series_type = data.get('statisticalValue')
        series_name = data.get('seriesName')
        series_score = data.get('seriesScore')
        every_hit_score = data.get('everyHitScore')
        frequency = data.get('frequency')
        # 使用PyMysql方式查询数据库,使用cursor（）方法获取操作游标
        con = utils.connect_mysql()
        cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            # sql 查询语句
            sql = """insert into series(plan_id,series_name,series_score, everyhit_score,frequency,series_type) values 
                   ('%s','%s','%s','%s','%s','%s')""" % (plan_id, series_name, series_score, every_hit_score,
                                                         frequency, series_type)
            print(sql)
            cursor.execute(sql)
            con.commit()
            # 计算方案总分且入库
            plan_total_score(plan_id)
            result = {'code': 200, 'data': "新增成功！"}
        except exception as e:
            con.rollback()
            result = {'code': 400, 'data': str(e)}
        cursor.close()
        con.close()
    else:
        result = '请使用post请求！'
    return JsonResponse({'result': result})


# 编辑组别信息
def update_series(request):
    if request.method == "POST":
        data = request.POST
        plan_id = data.get('planId')
        series_id = data.get('seriesId')
        series_name = data.get('seriesName')
        series_score = data.get('seriesScore')
        every_hit_score = data.get('everyHitScore')
        frequency = data.get('frequency')
        # 使用PyMysql方式查询数据库,使用cursor（）方法获取操作游标
        con = utils.connect_mysql()
        cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            # sql修改语句
            sql = """update series set series_name = '%s',series_score = '%s',everyhit_score = '%s',
                     frequency = '%s' where series_id = '%s'""" \
                     % (series_name, series_score, every_hit_score, frequency, series_id)
            print(sql)
            cursor.execute(sql)
            con.commit()
            plan_total_score(plan_id)
            result = {'code': 200, 'data': '修改成功'}
        except exception as e:
            con.rollback()
            result = {'code': 400, 'data': str(e)}
        cursor.close()
        con.close()
    else:
        result = {'code': 400, 'data': '请使用post请求！'}
    return JsonResponse({'result': result})


# 删除组别信息
def delete_series(request):
    if request.method == 'POST':
        data = request.POST
        plan_id = data.get('planId')
        series_id = data.get('seriesId')
        # 使用PyMysql方式查询数据库,使用cursor（）方法获取操作游标
        con = utils.connect_mysql()
        cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            # sql 删除语句
            sql = """delete from series where series_id = '%s'""" % series_id
            print(sql)
            cursor.execute(sql)
            con.commit()
            plan_total_score(plan_id)
            result = {'code': 200, 'data': '删除成功！'}
        except exception as e:
            con.rollback()
            result = {'code': 400, 'data': str(e)}
        cursor.close()
        con.close()
    else:
        result = {'code': 400, 'data': '请使用POST请求！'}
    return JsonResponse({'result': result})


# 批量删除组别信息
def batch_delete_series(request):
    if request.method == "POST":
        data = request.POST
        plan_id = data.get("planId")
        series_ids = data.getlist('seriesIds')
        series_ids = ','.join(series_ids)
        print(series_ids)
        # 使用PyMysql方式查询数据库,使用cursor（）方法获取操作游标
        con = utils.connect_mysql()
        cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            # sql 批量删除语句
            sql = """delete from series where series_id in (%s)""" % series_ids
            print(sql)
            cursor.execute(sql)
            con.commit()
            plan_total_score(plan_id)
            result = {'code': 200, 'data': '批量删除成功！'}
        except exception as e:
            con.rollback()
            result = {'code': 400, 'result': str(e)}
    else:
        result = {'code': 400, 'data': '请使用POST请求！'}
    return JsonResponse({'result': result})


# 上传接口
def upload_series(request):
    if request.method == "POST":
        data = request.POST
        obj = request.FILES.get('file')
        try:
            f = open(os.path.join(series_path, obj.name), 'wb')
            for chunk in obj.chunks():
                f.write(chunk)
            f.close()
            result = {'code': 200, 'data': "上传成功！"}
        except exception as e:
            result = {'code': 400, 'data': str(e)}
    else:
        result = '请使用post请求！'
    return JsonResponse({'result': result})


# 新增关键词
def create_keyword(request):
    if request.method == "POST":
        data = request.POST
        series_id = data.get('seriesId')
        key_word = data.get('keyWord')
        homophonic_word = data.getlist('homophonicWord')
        homophonic_word = ','.join(homophonic_word)
        related_word = data.get('relatedWord')
        second = data.get('second')
        # 使用PyMysql方式查询数据库,使用cursor（）方法获取操作游标
        con = utils.connect_mysql()
        cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            # sql 查询语句
            sql = """insert into keyword(series_id,key_word,homophonic_word, related_word,second) values 
            ('%s','%s','%s','%s','%s')""" % (series_id, key_word, homophonic_word, related_word, second)
            print(sql)
            cursor.execute(sql)
            con.commit()
            result = {'code': 200, 'data': "新增成功！"}
        except exception as e:
            con.rollback()
            result = {'code': 400, 'data': str(e)}
        cursor.close()
        con.close()
    else:
        result = '请使用post请求！'
    return JsonResponse({'result': result})


# 关键词列表
def key_word_list(request):
    if request.method == 'POST':
        data = request.POST
        series_id = data.get('seriesId')
        page_num = data.get('pageNum')
        page_num = int(page_num)
        page_size = data.get('pageSize')
        page_size = int(page_size)
        page_count = (page_num - 1) * page_size
        # 使用PyMysql方式查询数据库,使用cursor（）方法获取操作游标
        con = utils.connect_mysql()
        cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            sql = """select keyword_id as keywordId,series_id as seriesId, key_word as keyWord,
                     homophonic_word as homophonicWord, related_word as relatedWord, second
                     from keyword where series_id = '%s'""" % series_id
            sql_total = """select count(*) as total from keyword where series_id = '%s'""" % series_id
            sql += """order by keyword.keyword_id desc limit %s,%s""" % (page_count, page_size)
            print(sql)
            cursor.execute(sql)
            result_list = cursor.fetchall()
            print(sql_total)
            cursor.execute(sql_total)
            result_total = cursor.fetchall()
            cursor.close()
            if not result_list:
                results = []
            else:
                for dict in result_list:
                    homophonic_Word = dict.get('homophonicWord')
                    # 谐音词字符串转list
                    homophonic_Word = homophonic_Word.split(",")
                    dict['homophonicWord'] = homophonic_Word
            for i in result_total:
                total = i.get('total')
            results = {"content": result_list, 'total': total}
            result = {'code': 200, 'data': results}
        except exception as e:
            result = {'code': 400, 'data': str(e)}
        cursor.close()
        con.close()
    else:
        print('请使用post请求！')
    return JsonResponse({'result': result})


# 上一个组别
def last_series(request):
    if request.method == 'POST':
        data = request.POST
        series_id = data.get('seriesId')
        plan_id = data.get('planId')
        # 使用PyMysql方式查询数据库,使用cursor（）方法获取操作游标
        con = utils.connect_mysql()
        cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            sql = """select series_id as seriesId,series_name as seriesName from series
                        where series_id=(select max(series_id) from series 
                        where series_id< '%s' and plan_id = '%s')""" % (series_id, plan_id)
            print(sql)
            cursor.execute(sql)
            results = cursor.fetchall()
            print(results)
            if not results:
                result = {'code': 400, 'data': '没有上一条啦！'}
            else:
                result = {'code': 200, 'data': results}
        except exception as e:
            result = {'code': 400, 'data': str(e)}
        cursor.close()
        con.close()
    else:
        print('请使用post请求！')
    return JsonResponse({'result': result})


# 下一个组别
def next_series(request):
    if request.method == 'POST':
        data = request.POST
        series_id = data.get('seriesId')
        plan_id = data.get('planId')
        # 使用PyMysql方式查询数据库,使用cursor（）方法获取操作游标
        con = utils.connect_mysql()
        cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            sql = """select series_id as seriesId,series_name as seriesName from series
                        where series_id=(select min(series_id) from series 
                        where series_id > '%s' and plan_id = '%s')""" % (series_id, plan_id)
            print(sql)
            cursor.execute(sql)
            results = cursor.fetchall()
            print(results)
            if not results:
                result = {'code': 400, 'data': '没有上一条啦！'}
            else:
                result = {'code': 200, 'data': results}
        except exception as e:
            result = {'code': 400, 'data': str(e)}
        cursor.close()
        con.close()
    else:
        print('请使用post请求！')
    return JsonResponse({'result': result})


# 编辑关键词
def edit_keyword(request):
    if request.method == "POST":
        data = request.POST
        keyword_id = data.get('keywordId')
        key_word = data.get('keyWord')
        homophonic_word = data.getlist('homophonicWord')
        homophonic_word = ','.join(homophonic_word)
        related_word = data.get('relatedWord')
        second = data.get('second')
        # 使用PyMysql方式查询数据库,使用cursor（）方法获取操作游标
        con = utils.connect_mysql()
        cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            # sql 查询语句
            sql = """update keyword set key_word = '%s',homophonic_word = '%s',related_word = '%s',
                  second = '%s' where keyword_id = '%s' """ % (key_word,homophonic_word,related_word,second,keyword_id)
            print(sql)
            cursor.execute(sql)
            con.commit()
            result = {'code': 200, 'data': "新增成功！"}
        except exception as e:
            con.rollback()
            result = {'code': 400, 'data': str(e)}
        cursor.close()
        con.close()
    else:
        result = '请使用post请求！'
    return JsonResponse({'result': result})


# 删除关键词
def delete_keyword(request):
    if request.method == 'POST':
        data = request.POST
        keyword_id = data.get('keywordId')
        # 使用PyMysql方式查询数据库,使用cursor（）方法获取操作游标
        con = utils.connect_mysql()
        cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            # sql 删除语句
            sql = """delete from keyword where keyword_id = '%s'""" % keyword_id
            print(sql)
            cursor.execute(sql)
            con.commit()
            result = {'code': 200, 'data': '删除成功！'}
        except exception as e:
            con.rollback()
            result = {'code': 400, 'data': str(e)}
        cursor.close()
        con.close()
    else:
        result = {'code': 400, 'data': '请使用POST请求！'}
    return JsonResponse({'result': result})


# 批量删除关键词
def batch_delete_keyword(request):
    if request.method == "POST":
        data = request.POST
        keyword_ids = data.getlist('keywordIds')
        keyword_ids = ','.join(keyword_ids)
        print(keyword_ids)
        # 使用PyMysql方式查询数据库,使用cursor（）方法获取操作游标
        con = utils.connect_mysql()
        cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            # sql 批量删除语句
            sql = """delete from keyword where keyword_id in (%s)""" % keyword_ids
            print(sql)
            cursor.execute(sql)
            con.commit()
            result = {'code': 200, 'data': '批量删除成功！'}
        except exception as e:
            con.rollback()
            result = {'code': 400, 'result': str(e)}
        cursor.close()
        con.close()
    else:
        result = {'code': 400, 'data': '请使用POST请求！'}
    return JsonResponse({'result': result})


