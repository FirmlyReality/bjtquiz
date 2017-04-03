#coding=utf-8

from functools import wraps
from Http.JsonResponse import *
from django.contrib.auth import *
from django.shortcuts import render,redirect

def RequestMethods(*methods):
    def Delegator(func):
        def wrapper(*args, **kwargs):
            for method in methods:
                if args[0].method == method:
                    return func(*args, **kwargs)
            else:
                return JsonResponse(False, "HTTP方法不支持!")
        return wrapper
    return Delegator
