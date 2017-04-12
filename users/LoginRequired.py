#coding=utf-8

from functools import wraps
from django.contrib.auth import *
from django.shortcuts import render,redirect
from django.http import HttpResponse

def LoginRequired(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		if args[0].user.is_authenticated():
			return func(*args, **kwargs)
		else:
			return redirect('/login/')
	return wrapper

def AdminRequired(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		if args[0].user.is_admin:
			return func(*args, **kwargs)
		else:
			return HttpResponse("<script type='text/javascript'>alert('抱歉，您不是管理员。');window.history.back();</script>")
	return wrapper
