#!/usr/bin/env python
# _*_ coding:utf-8 _*_
"""
@time: 2021/4/25 9:07
@author:donglongfei
@file: planSqlMethod.py
"""
from django.db.models import Sum

from qualityApp import models


# 修改方案总分
def plan_total_score(plan_id):
    """
    根据组别计算方案总分
    :param plan_id:
    :return: boolean
    """
    # 查询组别总分
    total_score = models.series.objects.filter(plan_id=plan_id).aggregate(sum=Sum('series_score'))
    total_score = total_score["sum"]
    # 方案总分入库
    models.plan.objects.filter(plan_id=plan_id).update(total_score=total_score)
    return True

