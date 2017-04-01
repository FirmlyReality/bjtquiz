from django.shortcuts import render,redirect
from weibo import APIClient

APP_KEY = '2411916390' # app key

CALLBACK_URL = 'http://120.25.241.20/main/' # callback url


secret_file = open("secret.txt")
APP_SECRET = secret_file.read().strip()
secret_file.close()

# Create your views here.

def index(request):
    return render(request,'index.html')

def login(request):
    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    url = client.get_authorize_url()
    return redirect(url)

def main(request):
    code = request.GET.get('code')
    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    r = client.request_access_token(code)
    access_token = r.access_token
    expires_in = r.expires_in
    client.set_access_token(access_token, expires_in)
    res = client.users.show.get()
    print(res)
    return render(request, profile_url = res['profile_image_url'], 'main.html')
