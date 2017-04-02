#coding=utf-8

from functools import wraps
from django.contrib.auth import *
from django.shortcuts import render,redirect

def LoginRequired(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		if args[0].user.is_authenticated():
			return func(*args, **kwargs)
		else:
			return redirect('/login/')
	return wrapper
