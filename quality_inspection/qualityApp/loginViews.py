#!/usr/bin/env python
# _*_ coding:utf-8 _*_
"""
@time: 2021/3/7 9:40
@author:donglongfei
@file: loginViews.py
"""
from __future__ import unicode_literals
# Create your views here
import json

from django.http import JsonResponse, HttpResponse


from qualityApp.models import user


# 登录装饰器
def login_required(view_func):
    """
    登陆装饰器
    :param view_func:
    :return:
    """
    def wrapper(request, *view_args, **view_kwargs):
        response = {}
        if request.COOKIES.get("userName", None):
            name = request.COOKIES.get("userName", None)
            print('get cookie [{}]'.format(name))
        # 判断用户是否登录,session验证
        if request.session.get("is_login", None):
            name = request.session.get("userName", None)
            print('get session userName is [{}]'.format(name))
            return view_func(request, *view_args, **view_kwargs)
        else:
            # 用户未登录,返回信息
            response['msg'] = '请登录！'
            response['code'] = '301'
            return JsonResponse(response)
    return wrapper


# 注册
def register(request):
    error = []
    account = None
    password = None
    password2 = None
    compare_flag = False
    data = request.POST
    if not data:
        data = request.GET
    if not data.get("account"):
        error.append("用户名不能为空！")
    else:
        account = data.get("account")
    if not data.get("password"):
        error.append("密码不能为空")
    else:
        password = data.get("password")
    if not data.get("password2"):
        error.append("确认密码不能为空")
    else:
        password2 = data.get("password")
    if password is not None:
        if password == password2:
            compare_flag = True
        else:
            error.append("两次输入密码不一致")
    if account is not None and password is not None and password2 is not None and compare_flag:
        user_obj = user.objects.create(user_name=account, password=password)
        user_obj.save()
        result = {'code': 200, 'data': '用户创建成功！'}
    else:
        result = {'code': 400, 'data': error}
    return JsonResponse({'result': result})


# 登陆
def my_login(request):
    error = []
    res = HttpResponse()
    username = None
    password = None
    data = request.POST
    if data:
        if not data.get("username"):
            error.append("用户名不能为空！")
        else:
            username = data.get("username")
        if not data.get("password"):
            error.append("密码不能为空!")
        else:
            password = data.get("password")
        if username is not None and password is not None:
            user_obj = user.objects.filter(user_name__exact=username, password__exact=password).values('user_id')
            if user_obj:
                request.session['is_login'] = True
                request.session['username'] = username
                user_id = user_obj[0].get("user_id")
                result = {'code': 200, 'data': '登陆成功'}
                res.content = json.dumps(result)
                res.set_cookie('userId', user_id)
                res.set_cookie('userName', username)
            else:
                result = {'code': 400, 'data': '用户不存在'}
                res.content = json.dump(result)
    else:
        result = {'code': 400, 'data': '请使用POST请求'}
        res.content = json.dump(result)
    return res


# 退出
def login_out(request):
    request.session.clear()
    result = {'code': 200, 'data': '退出成功'}
    return JsonResponse({'result': result})




