from django.shortcuts import render,redirect
from weibo import APIClient

APP_KEY = '2411916390' # app key
APP_SECRET = '03cb65de1861da7bbab19d68144e6de8' # app secret
CALLBACK_URL = 'https://github.com/FirmlyReality' # callback url

# Create your views here.

def index(request):
    return render(request,'index.html')

def login(request):
    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    url = client.get_authorize_url()
    return redirect(url)
