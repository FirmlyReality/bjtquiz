#-*- coding:utf-8 -*-
from django.shortcuts import render,redirect
from weibo import APIClient
from users.LoginRequired import *
from users.models import *
from Http.RequestMethods import *

# Create your views here.
@RequestMethods("GET")
def index(request):
    return render(request,'index.html')

@LoginRequired
@RequestMethods("GET")
def main(request):
    user = request.user
    return render(request, 'main.html', {'profile_url':user.avatar_hd, 'user_name':user.name })
