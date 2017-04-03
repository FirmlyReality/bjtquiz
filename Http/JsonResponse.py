#coding=utf-8

from django.http import HttpResponse
import json

def JsonResponse(is_success, message, data=None):
	if(data == None):
		jsonstr = json.dumps({'success':is_success, 'message': message})
	else:
		jsonstr = json.dumps({'success':is_success, 'message': message, 'data':data})
	return HttpResponse((jsonstr+'\n').decode("raw_unicode_escape"), content_type = "text/json")
