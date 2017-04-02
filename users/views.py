#-*- coding:utf-8 -*-
from django.shortcuts import render,redirect
from User.models import *
from django.contrib.auth import *
from User.LoginRequired import *

APP_KEY = '2411916390' # app key
CALLBACK_URL = 'http://120.25.241.20/loginback/' # callback url

secret_file = open("secret.txt")
APP_SECRET = secret_file.read().strip()
secret_file.close()


# Create your views here.
def login(request):
    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    url = client.get_authorize_url()
    return redirect(url)

def loginback(request):
    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    code = request.GET.get('code')
    r = client.request_access_token(code)
    access_token = r.access_token
    expires_in = r.expires_in
    uid = r.uid
    client.set_access_token(access_token, expires_in)
    res = client.users.show.get(uid=uid)
    print(res)
    user = authenticate(uid=uid,password=" ")
    if user is None:
        user = MyUser.objects.create_user(uid," ",res.name, res.avatar_hd , access_token, expires_in)
    else:
        user.avatar_hd = res.avatar_hd
        user.name = res.name
        user.save()
    login(request, user)
    return redirect('/main/')

@LoginRequired
def logout(request):
    logout(request)
    return redirect('/')
