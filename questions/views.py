from django.shortcuts import render,redirect
from weibo import APIClient

APP_KEY = '2411916390' # app key
CALLBACK_URL = 'http://120.25.241.20/main/' # callback url


secret_file = open("secret.txt")
APP_SECRET = secret_file.read()
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
    print(client.statuses.user_timeline.get())
    return render(request,'main.html')
