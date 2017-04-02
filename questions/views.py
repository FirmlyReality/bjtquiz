#-*- coding:utf-8 -*-
from django.shortcuts import render,redirect
from weibo import APIClient
from users.LoginRequired import *
from users.models import *

# Create your views here.

def index(request):
    return render(request,'index.html')

@LoginRequired
def main(request):
    user = request.user
    return render(request, 'main.html', {'profile_url':user.avatar_hd, 'user_name':user.name })
