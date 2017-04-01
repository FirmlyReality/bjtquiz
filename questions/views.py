from django.shortcuts import render,redirect
from weibo import APIClient

APP_KEY = '2411916390' # app key
CALLBACK_URL = 'https://github.com/FirmlyReality' # callback url


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
