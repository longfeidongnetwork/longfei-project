#!/usr/bin/env python
# _*_ coding:utf-8 _*_
"""
@time: 2021/3/10 9:47
@author:donglongfei
@file: scoreLogicMethod.py
"""
import codecs
import ntpath
import os
from collections import Counter
from logging import exception
import pymysql
from qualityApp import utils
from qualityApp.scoreSqlMethod import select_series_info, select_series_list, insert_rating_details
from quality_inspection.settings import csv_path, daduan_path, dispute_path


# 逻辑一谐音词列表
def select_first_logic(plan_id):
    """
    逻辑一：只有关键词，谐音词，时长为0，没有关联词，判定为逻辑一
    :param plan_id: 方案名称id
    :return: 谐音词列表
    """
    # 逻辑一谐音词列表
    first_logic = []
    # plan_id = request.GET.get("plan_id")
    # 使用PyMysql方式查询数据库,使用cursor（）方法获取操作游标
    con = utils.connect_mysql()
    cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        # sql 查询语句
        sql = """select homophonic_word,series_type,series_name from keyword k left join series s on 
                 s.series_id = k.series_id left join plan p on s.plan_id = p.plan_id where k.related_word ="" and 
                 k.second = "0" and p.plan_id = '%s' """ % plan_id
        print(sql)
        cursor.execute(sql)
        result = cursor.fetchall()
        for i in result:
            # 谐音词，组别名，加减分法
            homophonic = i.get("homophonic_word")
            series_name = i.get("series_name")
            series_type = i.get("series_type")
            # 谐音词内容只有一个词组
            if ',' not in homophonic:
                first_logic.append(i)
            else:
                # 谐音词内容为多个词组
                words = homophonic.split(',')
                for key in words:
                    first_logic.append({"homophonic_word": key, "series_type": series_type, "series_name": series_name})
        cursor.close()
    except exception as e:
        print(e)
        con.rollback()
    con.close()
    print(first_logic)
    return first_logic


# 逻辑二谐音词列表
def select_second_logic(plan_id):
    """
    逻辑二；有关键词，有谐音词，有时长且为正，无关联词。判定为逻辑二
    :param plan_id: 方案名称id
    :return: second_logic: 逻辑二列表
    """
    # 逻辑二谐音词列表
    second_logic = []
    # plan_id = request.GET.get("plan_id")
    # 使用PyMysql方式查询数据库,使用cursor（）方法获取操作游标
    con = utils.connect_mysql()
    cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        # sql 查询语句
        sql = """select homophonic_word,series_type,series_name,second from keyword k left join series s on 
                 s.series_id = k.series_id left join plan p on s.plan_id = p.plan_id where k.related_word ="" and 
                 k.second > "0" and p.plan_id = '%s' """ % plan_id
        print(sql)
        cursor.execute(sql)
        result = cursor.fetchall()
        for i in result:
            # 谐音词，组别名，加减分法，时长
            homophonic = i.get("homophonic_word")
            series_name = i.get("series_name")
            series_type = i.get("series_type")
            second = i.get("second")
            # 谐音词内容只有一个词组
            if ',' not in homophonic:
                second_logic.append(i)
            else:
                # 谐音词内容为多个词组
                words = homophonic.split(',')
                for key in words:
                    second_logic.append({"homophonic_word": key, "series_type": series_type,
                                         "series_name": series_name, "second": second})
        cursor.close()
    except exception as e:
        print(e)
        con.rollback()
    con.close()
    print(second_logic)
    return second_logic


# 逻辑三谐音词列表
def select_third_logic(plan_id):
    """
    逻辑三；有关键词，有谐音词，有时长，有关联词。判定为逻辑三
    :param plan_id: 方案名称id
    :return: second_logic: 逻辑三列表
    """
    # 逻辑三谐音词列表
    third_logic = []
    # plan_id = request.GET.get("plan_id")
    # 使用PyMysql方式查询数据库,使用cursor（）方法获取操作游标
    con = utils.connect_mysql()
    cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        # sql 查询语句
        sql = """select homophonic_word,series_type,series_name,second,related_word from keyword k left join series s
                 on s.series_id = k.series_id left join plan p on s.plan_id = p.plan_id where k.related_word != ""
                 and p.plan_id = '%s' """ % plan_id
        print(sql)
        cursor.execute(sql)
        result = cursor.fetchall()
        for i in result:
            # 谐音词，组别名，加减分法,时长，关联词
            homophonic = i.get("homophonic_word")
            series_name = i.get("series_name")
            series_type = i.get("series_type")
            second = i.get("second")
            related_word = i.get("related_word")
            # 谐音词内容只有一个词组
            if ',' not in homophonic:
                third_logic.append(i)
            else:
                # 谐音词内容为多个词组
                words = homophonic.split(',')
                for key in words:
                    third_logic.append({"homophonic_word": key, "series_type": series_type,
                                        "series_name": series_name, "second":second, "related_word": related_word})
        cursor.close()
    except exception as e:
        print(e)
        con.rollback()
    con.close()
    print(third_logic)
    return third_logic


# 用逻辑一质检文件
def quality_first_logic(first_logic, data_list):
    """
    对一个文件使用逻辑一质检
    :param first_logic: 逻辑一
    :param data_list: lrc文件内容
    :return:result_first_logic
    """
    # 加法字典及加分法组字典
    addition = {}
    addition_group = {}
    # 减法字典及减分法组字典
    deduction = {}
    deduction_group = {}
    # 组别与关键词对应关系字典
    series_keyword = {}
    # 遍历逻辑一谐音词
    for homophonic in first_logic:
        for data in data_list:
            # 文件中含有逻辑一的谐音词
            if homophonic["homophonic_word"] in data:
                # 组别中出现的关键词列表
                series_keyword.setdefault(homophonic['series_name'], []).append(homophonic["homophonic_word"])
                # 行前时间 例:00:10.00
                position = data.split(']')[0][1:]
                # series_type为1是加分法
                if int(homophonic["series_type"]) == 1:
                    # 加分法命中的谐音词列表 key为谐音词，value为出现时间
                    addition.setdefault(homophonic['homophonic_word'], []).append(position)
                    # key命中的组别列表，value可统计一个组别出现的次数
                    addition_group.setdefault(homophonic['series_name'], []).append(position)
                # 否则为减分法
                else:
                    # 减分法命中的谐音词列表 key为谐音词，value为出现时间
                    deduction.setdefault(homophonic['homophonic_word'], []).append(position)
                    # key命中的组别列表，value可统计一个组别出现的次数
                    deduction_group.setdefault(homophonic['series_name'], []).append(position)
    result_first_logic = [addition, addition_group, deduction, deduction_group, series_keyword]
    return result_first_logic


# 用逻辑二质检文件
def quality_second_logic(second_logic, data_list):
    """
    对一个文件使用逻辑一质检
    :param second_logic: 逻辑一
    :param data_list: lrc文件内容
    :return:result_first_logic
    """
    # 加法字典及加分法组字典
    addition = {}
    addition_group = {}
    # 减法字典及减分法组字典
    deduction = {}
    deduction_group = {}
    # 组别与关键词对应关系字典
    series_keyword = {}
    # 遍历逻辑一谐音词
    for homophonic in second_logic:
        for data in data_list:
            # 文件中含有逻辑一的谐音词
            if homophonic["homophonic_word"] in data:
                # 组别中出现的关键词列表
                series_keyword.setdefault(homophonic['series_name'], []).append(homophonic["homophonic_word"])
                # 行前时间 例:00:10.00
                position = data.split(']')[0][1:]
                # series_type为1是加分法
                if int(homophonic["series_type"]) == 1:
                    # 加分法命中的谐音词列表 key为谐音词，value为出现时间
                    addition.setdefault(homophonic['homophonic_word'], []).append(position)
                    # key命中的组别列表，value可统计一个组别出现的次数
                    addition_group.setdefault(homophonic['series_name'], []).append(position)
                # 否则为减分法
                else:
                    # 减分法命中的谐音词列表 key为谐音词，value为出现时间
                    deduction.setdefault(homophonic['homophonic_word'], []).append(position)
                    # key命中的组别列表，value可统计一个组别出现的次数
                    deduction_group.setdefault(homophonic['series_name'], []).append(position)
    result_first_logic = [addition, addition_group, deduction, deduction_group, series_keyword]
    return result_first_logic


# 用逻辑三质检文件
def quality_third_logic(third_logic, data_list):
    """
    对一个文件使用逻辑一质检
    :param third_logic: 逻辑一
    :param data_list: lrc文件内容
    :return:result_first_logic
    """
    # 加法字典及加分法组字典
    addition = {}
    addition_group = {}
    # 减法字典及减分法组字典
    deduction = {}
    deduction_group = {}
    # 组别与关键词对应关系字典
    series_keyword = {}
    # 遍历逻辑一谐音词
    for homophonic in third_logic:
        for data in data_list:
            # 文件中含有逻辑一的谐音词
            if homophonic["homophonic_word"] in data:
                # 组别中出现的关键词列表
                series_keyword.setdefault(homophonic['series_name'], []).append(homophonic["homophonic_word"])
                # 行前时间 例:00:10.00
                position = data.split(']')[0][1:]
                # series_type为1是加分法
                if int(homophonic["series_type"]) == 1:
                    # 加分法命中的谐音词列表 key为谐音词，value为出现时间
                    addition.setdefault(homophonic['homophonic_word'], []).append(position)
                    # key命中的组别列表，value可统计一个组别出现的次数
                    addition_group.setdefault(homophonic['series_name'], []).append(position)
                # 否则为减分法
                else:
                    # 减分法命中的谐音词列表 key为谐音词，value为出现时间
                    deduction.setdefault(homophonic['homophonic_word'], []).append(position)
                    # key命中的组别列表，value可统计一个组别出现的次数
                    deduction_group.setdefault(homophonic['series_name'], []).append(position)
    result_first_logic = [addition, addition_group, deduction, deduction_group, series_keyword]
    return result_first_logic


# 加分法得分
def awarded_marks(first_addition_group, second_addition_group, third_addition_group, plan_id):
    """
    根据每个组别命中次数统计加分法的总分
    :param first_addition_group: 逻辑一中每个组别命中次数
    :param second_addition_group: 逻辑二中每个组别命中次数
    :param third_addition_group: 逻辑三中每个组别命中次数
    :param plan_id: 方案id
    :return: score 加分法得分
    """
    # 查询该方案下的组别名,总分,命中计分,出现次数等
    series_list = select_series_info(plan_id)
    # 统计每个逻辑组别命中次数
    for addition in [first_addition_group, second_addition_group, third_addition_group]:
        for j in addition:
            addition[j] = len(addition[j])
    # 将三个逻辑的组别合并 例{'组别1': 5, '组别2': 6}
    first_addition_group, second_addition_group, third_addition_group = \
        Counter(first_addition_group), Counter(second_addition_group), Counter(third_addition_group)
    group_hit = dict(first_addition_group+second_addition_group+third_addition_group)
    print(group_hit)
    # 得分 加分法：从0开始向上叠加
    score = 0
    rating_list = []
    for i in group_hit:
        for j in series_list:
            if i == j.get("series_name"):
                # 将组别与得分写入字典
                if group_hit[i] < j.get("frequency"):
                    group_score = group_hit[i] * j.get("everyhit_score")
                else:
                    group_score = j.get("series_score")
                score += group_score
                group_dict = i + ":" + str(group_score)
                rating_list.append(group_dict)
    return score, rating_list


# 减分法得分
def subtract_marks(first_deduction_group, second_deduction_group, third_deduction_group, plan_id):
    """
    根据每个组别命中次数统计减分法的总分
    :param first_deduction_group: 逻辑一中每个组别命中减分法总数
    :param second_deduction_group: 逻辑二中每个组别命中减分法总数
    :param third_deduction_group: 逻辑三中每个组别命中减分法总数
    :param plan_id: 方案id
    :return: score 得分
    """
    # 查询该方案下的组别名,总分,命中计分,出现次数等
    score, series_list = select_series_list(plan_id)
    print(series_list, score)
    # 统计每个逻辑组别命中次数
    for addition in [first_deduction_group, second_deduction_group, third_deduction_group]:
        for j in addition:
            addition[j] = len(addition[j])
    # 将三个逻辑的组别合并 例{'组别1': 5, '组别2': 6}
    first_deduction_group, second_deduction_group, third_deduction_group = \
        Counter(first_deduction_group), Counter(second_deduction_group), Counter(third_deduction_group)
    group_hit = dict(first_deduction_group + second_deduction_group + third_deduction_group)
    print(group_hit)
    rating_list = []
    # 减分法：从总分开始向下减分
    score = 0
    for j in series_list:
        for i in group_hit:
            if i == j.get("series_name"):
                # 将组别与得分写入组别
                if group_hit[i] < j.get("frequency"):
                    series_score = j.get("series_score")
                    group_score = group_hit[i] * j.get("everyhit_score")
                    get_score = series_score - group_score
                    score += get_score
                    group_dict = i + ":" + str(series_score-group_score)
                else:
                    score += 0
                    group_dict = i + ":" + str(0)
                rating_list.append(group_dict)
        # 如果减分项组别没有命中,则加分
        if j.get("series_name") not in group_hit.keys():
            group_score = j.get("series_score")
            score += group_score
            group_dict = j.get("series_name") + ":" + str(group_score)
            rating_list.append(group_dict)
    return score, rating_list


# 统计命中次数最多的关键词
def hit_top(first, second, third):
    """
    通过逻辑一，二，三中加分法和减分法谐音词字典，合并为key为关键词，值为出现次数的字典
    :param first: 逻辑一质检结果 first[0]加分法字典 first[2]减分法字典
    :param second:逻辑二质检结果 second[0] 加分法字典 second[2] 减分法字典
    :param third:逻辑三质检结果 third[0] 加分法字典 third[2]减分法字典
    :return:
    """
    for addition in [first[0], first[2], second[0], second[2], third[0], third[2]]:
        for j in addition:
            addition[j] = len(addition[j])
    first_i, first_j, second_i, second_j, third_i, third_j = Counter(first[0]), Counter(first[2]), Counter(second[0]), \
                                                             Counter(second[2]), Counter(third[0]), Counter(third[2])
    group_hit = dict(first_i + first_j + second_i + second_j + third_i + third_j)
    print(group_hit)
    hit_order = sorted(group_hit.items(), key=lambda x: x[1], reverse=True)
    return hit_order


# 每个组别命中的关键词
def keyword_classify(first, second, third):
    """
    将关键词与组别对应，便于查询
    :param first: 逻辑一组别与关键词对应关系
    :param second: 逻辑二组别与关键词对应关系
    :param third: 逻辑三组别与关键词对应关系
    :return: series_keyword
    """
    series_keyword = {}
    for series in [first, second, third]:
        for series_name, v in series.items():
            for keyword in v:
                series_keyword.setdefault(series_name, []).append(keyword)
    return series_keyword


# 写入csv文件
def create_csv_file(position, first, second, third):
    """
    将逻辑一逻辑二逻辑三质检后的关键词与时间对应关系写入csv文件，供页面查询
    :param position:
    :param first:
    :param second:
    :param third:
    :return:
    """
    csv_name = position[0] + '.csv'
    csv_name_path = os.path.join(csv_path,csv_name)
    if os.path.exists(csv_name_path):
        os.remove(csv_name_path)
    for key in [first[0], first[2], second[0], second[2], third[0], third[2]]:
        # 空的就不写了
        key = sorted(key.items(), key=lambda x: x[1], reverse=False)
        if len(key) > 1:
            with open(csv_name_path, 'a') as f:
                for k, v in key:
                    if v:
                        f.write(k + ',' + str(v) + '\n')
                    else:
                        f.write(k + '\n')


# 查询keyword对应时间
def get_keyword_time(keyword, csv_name):
    """
    根据keyword在csv文件中查询对应时间
    :param keyword:
    :param csv_name:
    :return: keyword_time
    """
    cav_name_path = os.path.join(csv_path, csv_name)
    with open(cav_name_path, 'r') as f:
        for line in f.readlines():
            print(line)
            if keyword == line.split(",")[0]:
                keyword_time = line.split(",")[1].replace('\n', '').replace('[', '').replace(']', '').replace("'", '')
    return keyword_time


# 打断扣分等
def deduct_mark(task_name, portion, score, data_list):
    """
    打断扣分，语速过快扣分，争辩扣分
    :param task_name:任务名称
    :param portion:
    :param score:得分
    :param data_list:
    :return:
    """
    rating_list = []
    try:
        # 打断扣分
        interrupt_file = daduan_path + task_name + '/' + portion[0] + '.csv'
        with open(interrupt_file, 'r') as f:
            csv_count = int(len(f.readlines()))
            if csv_count >= 5:
                score -= 5
                group_dict = 'interrupt' + ":" + str(0)
                rating_list.append(group_dict)
            else:
                score -= csv_count
                group_dict = 'interrupt' + ":" + str(5 - csv_count)
                rating_list.append(group_dict)
    except:
        pass
    try:
        speed = 2
        # 语速扣分
        count = 0  # 控制最多扣两分
        for i in data_list:
            i = i.replace('\n', '')
            speed = i.split(' ')[-1]
            if float(speed) > 7 and count < 2:
                score -= 1
                count += 1
                speed -= 1

        group_dict = 'interrupt' + ":" + str(speed)
        rating_list.append(group_dict)
    except:
        pass
    try:
        # 争论扣分
        dispute_file = dispute_path + task_name + '/' + portion[0] + '.csv'
        with open(dispute_file, 'r') as f:
            first_line = f.readlines()[0].replace('\n', '')
            if int(first_line) >= 10:
                group_dict = 'dispute' + ":" + str(0)
            else:
                dispute_score = 10 - int(first_line)
                group_dict = 'dispute' + ":" + str(dispute_score)
        rating_list.append(group_dict)
    except:  # 未找到文件就算满分
        group_dict = 'dispute' + ":" + str(10)
        rating_list.append(group_dict)
    return score, rating_list


# 所有lrc文件进行质检
def quality_lrc(lrc_list, plan_id):
    """
    对lrc文件质检
    :param lrc_list: lrc文件列表
    :param plan_id: 质检方案
    :return:
    """
    try:
        # 逻辑一谐音词列表
        first_logic = select_first_logic(plan_id)
        # 逻辑二谐音词列表
        second_logic = select_second_logic(plan_id)
        # 逻辑三谐音词列表
        third_logic = select_third_logic(plan_id)
        file_list = []
        # 将lrc路径格式化为一个列表
        for i in lrc_list:
            for file in i:
                file_list.append(file)
        # 遍历所有lrc文件路径
        for file in file_list:
            # 找到对应音频名
            filename = ntpath.basename(file)
            # 获取目录名
            path = os.path.normpath(file)
            s = path.split(os.sep)
            task_name = s[-2]
            portion = os.path.splitext(filename)
            # 读取lrc文件,获取文件内容
            file_read = codecs.open(file, 'r', encoding='utf-8')
            file_info = file_read.readlines()
            data_list = [x for x in file_info if '客服' in x]
            # 用逻辑一质检文件
            result_first_logic = quality_first_logic(first_logic, data_list)
            # 用逻辑二质检文件
            result_second_logic = quality_second_logic(second_logic, data_list)
            # 用逻辑三质检文件
            result_third_logic = quality_third_logic(third_logic, data_list)
            # 将关键词对应时间写入csv文件
            create_csv_file(portion, result_first_logic, result_second_logic, result_third_logic)
            # 统计加分法得分及加分法单独组别得分详情
            add_statistics_score, add_rating_list = awarded_marks(result_first_logic[1],
                                                                  result_second_logic[1], result_third_logic[1],
                                                                  plan_id)
            # 统计减分法得分及减分法单独组别得分详情
            sub_statistics_score, sub_rating_list = subtract_marks(result_first_logic[3],
                                                                   result_second_logic[3], result_third_logic[3],
                                                                   plan_id)
            score = add_statistics_score + sub_statistics_score
            # 统计打断，语速，争执，离席时间扣分
            mark = deduct_mark(task_name, portion, score)
            # 将组别得分详情入库
            rating_detail = add_rating_list + sub_rating_list
            # 统计命中次数最多的关键词
            hit_order = hit_top(result_first_logic, result_second_logic, result_third_logic)
            # 组别关键词对应信息
            series_keyword = keyword_classify(result_first_logic[4], result_second_logic[4], result_third_logic[4])
            print(series_keyword)
            if portion[1] == '.lrc':
                audio_name = portion[0] + '.wav'
            # 插入质检结果
            result = insert_rating_details(audio_name, task_name, plan_id, score, hit_order, rating_detail,
                                           series_keyword)
    except exception as e:
        print(e)
    return result


