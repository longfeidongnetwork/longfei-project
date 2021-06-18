#!/usr/bin/env python
# _*_ coding:utf-8 _*_
"""
@time: 2021/3/11 14:26
@author:donglongfei
@file: test.py
"""
import datetime

# storage={}
#
# storage['first']={}
# print(storage)
# storage['first'].setdefault('Grace',[]).append('sister')
# print(storage)
# tian='tian'
# storage['first'].setdefault('Grace',[]).append(tian)
#
# # print(r is storage['first']['Grace'])
# print(storage)


def get_date_list(begin_date, end_date):
    """
    获取一个月的时间列表
    :param begin_date:
    :param end_date:
    :return:
    """
    dates = []
    dt = datetime.datetime.strptime(begin_date, "%m-%d")
    date = begin_date[:]
    while date <= end_date:
        dates.append(date)
        dt += datetime.timedelta(days=1)
        date = dt.strftime("%m-%d")
    return dates


value = get_date_list("04-11", "05-11")
print(value)