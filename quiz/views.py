#-*- coding:utf-8 -*-
from django.shortcuts import render,redirect
from weibo import APIClient
from users.LoginRequired import *
from users.models import *
from Http.RequestMethods import *
from Http.JsonResponse import *
from quiz.models import *
import random,time
from datetime import datetime

# Create your views here.
@RequestMethods("GET")
def index(request):
    return render(request,'index.html')

#@LoginRequired
@RequestMethods("GET")
def main(request):
    user = request.user
    return render(request, 'main.html', {'user':user})

@RequestMethods("GET")
def finished(request):
    user = request.user
    return render(request, 'finished.html')

q1_num = 20
q2_num = 5
q3_num = 5
limit_time = 10

def addquestions(status, level, num):
    questions = Question.objects.filter(level=level).all()
    random.seed(time.time())
    indexes = random.sample(range(len(questions)), num)
    for i in indexes:
        status.questions.add(questions[i])

def getoptions(question,quizstatus):
    random.seed(time.time())
    indexs = random.sample(range(4), 4)
    options = {}
    in2an = ['A', 'B', 'C', 'D']
    i = 0
    for index in indexs:
        if index == 0:
            options[in2an[i]] = question.optionA
        elif index == 1:
            options[in2an[i]] = question.optionB
        elif index == 2:
            options[in2an[i]] = question.optionC
        elif index == 3:
            options[in2an[i]] = question.optionD
        if question.answer == in2an[index]:
            quizstatus.answer = in2an[i]
            quizstatus.save()
        i += 1
    return options

@LoginRequired
@RequestMethods("GET")
def quiz(request):
   global q1_num, q2_num, q3_num
   total = q1_num + q2_num + q3_num
   quizstatus = request.user.quizstatus
   if quizstatus.now_qnum == 0:
       addquestions(quizstatus, 1, q1_num)
       addquestions(quizstatus, 2, q2_num)
       addquestions(quizstatus, 3, q3_num)
       quizstatus.start_time = datetime.now()
       quizstatus.save()
   if quizstatus.is_finished == True:
       if quizstatus.now_qnum < total:
           quizstatus.now_qi = random.randint(0,29-quizstatus.now_qnum)
           now_question = quizstatus.questions.all()[quizstatus.now_qi]
           quizstatus.now_qnum += 1
           quizstatus.qtime = datetime.now()
           quizstatus.is_finished = False
           quizstatus.save()
           options = getoptions(now_question, quizstatus)
       else:
           history = QuizHistory(user=request.user, qnum=total, rightnum=quizstatus.now_rightnum)
           history.use_time = quizstatus.use_time
           history.save()
           quizstatus.now_qnum = 0
           quizstatus.delete()
           status = QuizStatus(user=request.user, now_qnum=0, now_rightnum=0, is_finished=True)
           status.qtime = datetime.now()
           status.start_time = datetime.now()
           status.save()
           print(history.use_time)
           mins = int(history.use_time/60000)
           secs = int(history.use_time%60000/1000)
           return render(request, 'finished.html', {'result':history, 'mins':mins, 'secs':secs})

   else:
       now_question = quizstatus.questions.all()[quizstatus.now_qi]
       options = getoptions(now_question, quizstatus)
   t = quizstatus.qtime.timetuple()
   timestamp = int(time.mktime(t))*1000
   return render(request, 'quiz.html', {'user':request.user, 'question':now_question.question, 'options':options, 'now_qnum':quizstatus.now_qnum, 'total':total, 'qtime':timestamp})

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
        question = quizstatus.questions.all()[quizstatus.now_qi]
        quizstatus.questions.remove(question)
        delta = datetime.now() - quizstatus.qtime
        dseconds = delta.seconds
        if delta.seconds >= limit_time:
            dseconds = limit_time
        quizstatus.use_time += int(dseconds*1000 + int(delta.microseconds/1000))
        quizstatus.save()
        if delta.seconds >= limit_time:
            return JsonResponse(False, "回答超时，请回答下一题！")
        else:
            print(option)
            print(question.answer)
            if option == quizstatus.answer:
                question.total += 1
                question.right += 1
                quizstatus.now_rightnum += 1
                quizstatus.save()
                question.save()
                return JsonResponse(True, "回答正确！")
            else:
                question.total += 1
                question.save()
                return JsonResponse(False,"回答错误！")

@LoginRequired
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

@LoginRequired
@AdminRequired
@RequestMethods('GET')
def admin_interface(request):
    return render(request, 'admin.html', {'user':request.user})

@LoginRequired
@AdminRequired
@RequestMethods('GET')
def history(request):
    histories =  QuizHistory.objects.order_by('-end_time').all()
    return render(request, 'history.html', {'user':request.user, 'histories':histories})
