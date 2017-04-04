#-*- coding:utf-8 -*-
from django.shortcuts import render,redirect
from weibo import APIClient
from users.models import *
from quiz.models import *
from django.contrib.auth import *
from users.LoginRequired import *
from Http.RequestMethods import *
from datetime import datetime

APP_KEY = '2411916390' # app key
CALLBACK_URL = 'http://120.25.241.20/loginback/' # callback url

secret_file = open("secret.txt")
APP_SECRET = secret_file.read().strip()
secret_file.close()


# Create your views here.
@RequestMethods("GET")
def weblogin(request):
    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    url = client.get_authorize_url()
    return redirect(url)

@RequestMethods("GET")
def webloginback(request):
    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    code = request.GET.get('code',None)
    if code is None:
        print("code is None")
        return redirect("/")
    r = client.request_access_token(code)
    access_token = r.access_token
    expires_in = r.expires_in
    uid = r.uid
    client.set_access_token(access_token, expires_in)
    res = client.users.show.get(uid=uid)
    user = authenticate(uid=uid,password=" ")
    if user is None:
        user = MyUser.objects.create_user(uid," ",res.name, res.avatar_hd , access_token, expires_in)
        status = QuizStatus(user=user, now_qnum=0, now_rightnum=0, is_finished=True)
        status.qtime = datetime.now()
        status.save()
    else:
        user.avatar_hd = res.avatar_hd
        user.name = res.name
        user.save()
    login(request, user)
    return redirect('/main/')

@LoginRequired
@RequestMethods("GET")
def weblogout(request):
    logout(request)
    return redirect('/')
