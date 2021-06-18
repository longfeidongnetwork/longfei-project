#!/usr/bin/env python
# _*_ coding:utf-8 _*_
"""
@time: 2021/3/9 17:46
@author:donglongfei
@file: scoreSqlMethod.py
"""
import os
from datetime import datetime
from logging import exception
import pymysql


# 根据录音的质检结果id 查询 录音id
from qualityApp import models, utils
from quality_inspection.settings import lrc_path, absolute_path


def select_record_id(result_id):
    """
    根据result_id查询record_id
    :param result_id:质检结果id
    :return: record_id 录音
    """
    # 使用PyMysql方式查询数据库,使用cursor（）方法获取操作游标
    con = utils.connect_mysql()
    cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        # sql 查询语句
        sql = """select record_id from result where result_id = '%s' """ % result_id
        print(sql)
        cursor.execute(sql)
        result = cursor.fetchone()
        record_id = result["record_id"]
    except exception as e:
        con.rollback()
    cursor.close()
    con.close()
    return record_id


# 根据任务名称id查询所有录音
def select_record_ids(task_ids, record_ids):
    """
    :查询该目录下的所有录音文件
    :param task_ids:任务id
    :param record_ids:音频id
    :return: lrc_list lrc文件列表
    """
    try:
        task = models.task.objects.filter(task_id__in=task_ids).values("task_name")
        task_name = task[0].get("task_name")
        path = os.path.join(lrc_path, task_name)
        record_list = models.record.objects.filter(record_id__in=record_ids).values("record_name")
        lrc_list = []
        for key in record_list:
            record_name = key["record_name"]
            portion = os.path.splitext(record_name)
            record_name = portion[0]
            file_path = utils.seek_files(record_name, path)
            lrc_list.append(file_path)
        print(record_list)
    except exception as e:
        print(e)
    return lrc_list


# 根据目录名称id查询所有lrc文件
def select_task_ids(task_ids):
    """
    :查询该目录下的所有lrc文件，数据库任务名称对应系统目录名
    :param task_ids:任务名称id
    :return: lrc_list
    """
    try:
        task_name_list = models.task.objects.filter(task_id__in=task_ids).values("task_name")
        print(task_name_list)
        # 所有目录下所有lrc文件
        lrc_list = []
        for key in task_name_list:
            task_name = key["task_name"]
            # 找到单个目录下的所有lrc文件
            file_path = utils.get_file(task_name, lrc_path)
            lrc_list.append(file_path)
    except exception as e:
        print(e)
    return lrc_list


# 查询组别加分列表
def select_series_info(plan_id):
    """
    查询所有组别的命中计分，出现次数等
    :param plan_id: 方案id
    :return: 组别列表
    """
    try:
        series_list = models.series.objects.filter(plan_id=plan_id, series_type=1).values()
        print(series_list)
    except exception as e:
        print(e)
    return series_list


# 查询组别减分列表
def select_series_list(plan_id):
    """
    查询所有组别的命中计分，出现次数等
    :param plan_id: 方案id
    :return: 组别列表
    """
    try:
        series_list = models.series.objects.filter(plan_id=plan_id, series_type=2).values()
        subtract_score = 0
        for i in series_list:
            subtract_score += i.get("series_score")
    except exception as e:
        print(e)
    return subtract_score, series_list


# 插入得分详情
def insert_rating_details(audio_name, task_name, plan_id, score, hit_order, rating_detail, series_keyword):
    """
    将质检得分插入数据库
    :param audio_name: 质检音频名
    :param plan_id: 质检方案id
    :param score: 质检总分
    :param hit_order: 关键词命中次数
    :param rating_detail: 组别得分详情
    :param series_keyword 组别关键词对应关系
    :return:result
    """
    try:
        task_id = models.task.objects.filter(task_name=task_name).values("task_id")
        task_id = task_id[0]["task_id"]
        record_id = models.record.objects.filter(record_name=audio_name,task_id=task_id).values("record_id")
        record_id = record_id[0]["record_id"]
        # 命中次数最多前三位入库
        key1 = ''
        if len(hit_order) > 0:
            key1 = hit_order[0][0]
        key2 = ''
        if len(hit_order) > 1:
            key2 = hit_order[1][0]
        key3 = ''
        if len(hit_order) > 2:
            key3 = hit_order[2][0]
        # 组别得分详情入库
        rating_detail = ';'.join(rating_detail)
        # 关键词去重入库
        for i in series_keyword:
            keywords = series_keyword[i]
            keywords = list(set(keywords))
            series_keyword[i] = keywords
        # 如果已经质检一次，则修改
        record = models.result.objects.filter(record_id=record_id)
        if record.exists():
            result = models.result.objects.filter(record_id=record_id).update(plan_id=plan_id, user_id=1, score=score,
                                                                              key1=key1, key2=key2, key3=key3,
                                                                              rating_details=rating_detail,
                                                                              series_keyword=series_keyword)
        else:
            # 将质检结果插入数据库
            result = models.result(record_id=record_id, plan_id=plan_id, user_id=1, score=score,key1=key1, key2=key2,
                                   key3=key3, rating_details=rating_detail, series_keyword=series_keyword)
            result.save()
        if result:
            result = True
    except exception as e:
        print(e)
    return result


# 查询评分详情
def select_rating_details(record_id):
    """
    查询评分详情
    :return:
    """
    try:
        result = models.result.objects.filter(record_id=record_id).values()
        plan_id = result[0].get("plan_id")
        plan = models.plan.objects.filter(plan_id=plan_id).values("plan_name")
        plan_name = plan[0]["plan_name"]
        rating_details = result[0].get("rating_details")
        series_keyword = result[0].get("series_keyword")
        score = result[0].get("score")
        if not rating_details:
            return rating_details, plan_name, score
        if not series_keyword:
            return rating_details, plan_name, score
        series_keyword = eval(series_keyword)
        print(series_keyword)
        rating_details = rating_details.split(";")
        rating = []
        for i in rating_details:
            series = i.split(":")
            series_name = series[0]
            c = dict()
            c["id"] = series_name
            word_list = []
            for key in series_keyword:
                if series_name == key:
                    for word in series_keyword[key]:
                        words = {"label": word}
                        word_list.append(words)
            c["keyword"] = word_list
            series_score = models.series.objects.filter\
                (plan_id=plan_id, series_name=series_name).values("series_score")
            c["totalScore"] = series_score[0].get("series_score")
            c["score"] = int(series[1])
            rating.append(c)
    except exception as e:
        print(e)
    return rating, plan_name, score


# 人工打分
def update_rating_details(record_id, score, series_params):
    """
    人工打分
    :param record_id: 音频id
    :param score: 得分
    :param series_params: 组别参数
    :return:
    """
    try:
        result = models.result.objects.filter(record_id=record_id).values()
        rating_details = result[0].get("rating_details")
        rating_details = rating_details.split(";")
        rating = []
        total_score = 0
        for i in rating_details:
            series = i.split(":")
            series_name = series[0]
            series_score = series[1]
            if series_params == series_name:
                group_dict = series_name + ":" + str(score)
                rating.append(group_dict)
                total_score += int(score)
            else:
                group_dict = series_name + ":" + str(series_score)
                rating.append(group_dict)
                total_score += int(series_score)
        rating_detail = ';'.join(rating)
        # 修改打分操作
        result = models.result.objects.filter\
            (record_id=record_id).update(rating_details=rating_detail, score=total_score)
        if result:
            result = True
    except exception as e:
        print(e)
    return result


# lrc文件内容
def get_lrc(record_id, task_id):
    """
    获取lrc文件内容
    :param record_id:
    :param task_id:
    :return:
    """
    record = models.record.objects.filter(record_id=record_id).values("record_name")
    record_name = record[0]["record_name"]
    portion = os.path.splitext(record_name)
    lrc_name = portion[0] + '.lrc'
    print(task_id)
    task = models.task.objects.filter(task_id=task_id).values("task_name")
    task_name = task[0]["task_name"]
    path = os.path.join(lrc_path, task_name, lrc_name)
    with open(path, 'r', encoding='utf-8') as f:
        data = f.read()
    print(data)
    return data


# lrc文件内容
def get_record(record_id, task_id):
    """
    获取音频文件路径
    :param record_id:
    :param task_id:
    :return:
    """
    record = models.record.objects.filter(record_id=record_id).values("record_name")
    record_name = record[0]["record_name"]
    task = models.task.objects.filter(task_id=task_id).values("task_name")
    task_name = task[0]["task_name"]
    record_path = os.path.join(absolute_path, task_name, record_name)
    return record_path


# 根据任务id查询任务名
def select_task_name(task_id):
    """
    查询任务名
    :param task_id:任务id
    :return:
    """
    # 使用PyMysql方式查询数据库,使用cursor（）方法获取操作游标
    con = utils.connect_mysql()
    cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        # sql 查询语句
        sql = """select task_name from task where task_id = '%s' """ % task_id
        print(sql)
        cursor.execute(sql)
        result = cursor.fetchone()
        task_name = result["task_name"]
    except exception as e:
        con.rollback()
    cursor.close()
    con.close()
    return task_name


# 根据id查文件名
def query_record_name(record_id):
    # 使用PyMysql方式查询数据库,使用cursor（）方法获取操作游标
    con = utils.connect_mysql()
    cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        # sql 查询语句
        sql = """select record_name from record where record_id = '%s'""" % record_id
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
