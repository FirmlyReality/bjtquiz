#-*- coding:utf-8 -*-
from django.shortcuts import render,redirect
from weibo import APIClient
from users.LoginRequired import *
from users.models import *
from Http.RequestMethods import *
from Http.JsonResponse import *
from quiz.models import *
import random
from datetime import datetime

# Create your views here.
@RequestMethods("GET")
def index(request):
    return render(request,'index.html')

@LoginRequired
@RequestMethods("GET")
def main(request):
    user = request.user
    return render(request, 'main.html', {'profile_url':user.avatar_hd, 'user_name':user.name })

q1_num = 20
q2_num = 5
q3_num = 5
limit_time = 10

def addquestions(status, level, num):
    questions = Question.objects.filter(level=level).all()
    indexes = randowm.sample(range(len(questions)), num)
    for i in indexes:
        status.questions.add(questions[i])

#@LoginRequired
@RequestMethods("GET")
def quiz(request):
   '''global q1_num, q2_num, q3_num
   total = q1_num + q2_num + q3_num
   quizstatus = reques.user.quizstatus
   if quizstatus.now_qnum == 0:
       addquestions(quizstatus, 1, q1_num)
       addquestions(quizstatus, 2, q2_num)
       addquestions(quizstatus, 3, q3_num)
       quizstatus.save()
   if quizstatus.is_finished == True:
       if quizstatus.now_qnum < total:
           now_question = quizstatus.questions.all()[quizstatus.now_qnum]
           quizstatus.now_qnum += 1
           quizstatus.qtime = datetime.now()
           quizstatus.is_finished = False
           quizstatus.save()
       else:
           history = QuizHistory(user=request.user, qnum=total, rightnum=quizstatus.now_rightnum)
           history.save()
           quizstatus.now_qnum = 0
           quizstatus.delete()
           status = QuizStatus(user=request.user, now_qnum=0, now_rightnum=0, is_finished=True)
           status.qtime = datetime.now()
           status.save()
           return render(request, 'finished.html', {'result':history})

   else:
       now_question = quizstatus.questions.all()[quizstatus.now_qnum-1]'''
   return render(request, 'quiz.html' )#{'question':now_question})

@LoginRequired
@RequestMethods("POST")
def submit(request):
    option = request.POST.get('option',None)
    if option is None:
        print("option is None")
        return redirect("/")
    quizstatus = request.user.quizstatus
    if quizstatus.is_finished:
        return JsonResponse(False, "你无法提交该题答案了。")
    else:
        quizstatus.is_finished = True
        quizstatus.save()
        if (datetime.now() - quizstatus.qtime).seconds > limit_time:
            return JsonResponse(False, "回答超时，请回答下一题！")
        else:
            question = quizstatus.questions.all()[quizstatus.now_qnum-1]
            if option == question.answer:
                question.total += 1
                question.right += 1
                question.save()
                return JsonResponse(True, "回答正确！")
            else:
                question.total += 1
                question.save()
                return JsonResponse(False,"回答错误！")

@RequestMethods("GET")
def readquestions(request):
    infile = open("questions.txt")
    lines = infile.readlines()
    i = 0
    level = 1
    while i < len(lines):
        info = lines[i].decode('GB2312')
        if info.encode('utf-8')[0:6] == '初级':
            level = 1
        elif info.encode('utf-8')[0:6] == '中级':
            level = 2
        elif info.encode('utf-8')[0:6] == '高级':
            level = 3
        else:
            if not info.strip() == "":
                questiontxt = info
                optionA = lines[i+1].decode('GB2312')[2:].strip()
                optionB = lines[i+2].decode('GB2312')[2:].strip()
                optionC = lines[i+3].decode('GB2312')[2:].strip()
                optionD = lines[i+4].decode('GB2312')[2:].strip()
                ans = lines[i+6].decode('GB2312')[0].strip()
                que = Question(question=questiontxt, optionA=optionA, optionB=optionB, optionC=optionC, optionD=optionD)
                que.answer = ans
                que.level = level
                que.total = 0
                que.right = 0
                que.save()
                print(questiontxt)
                print(optionA)
                print(optionB)
                print(optionC)
                print(optionD)
                print(ans)
                i += 6
        i += 1
    return redirect('/')
