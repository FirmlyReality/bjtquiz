from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Question(models.Model):
    question = models.TextField()
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    answer = models.CharField(max_length=5)
    level = models.IntegerField()
    total = models.BigIntegerField()
    right = models.BigIntegerField()

class QuizStatus(models.Model):
    user = models.OneToOneField('users.MyUser', on_delete=models.CASCADE, related_name='quizstatus')
    questions = models.ManyToManyField('quiz.Question', related_name='quizstatuses')
    now_qnum = models.IntegerField()
    now_rightnum = models.IntegerField()
    qtime = models.DateTimeField()
    is_finished = models.BooleanField()

class QuizHistory(models.Model):
    user = models.ForeignKey('users.MyUser', on_delete=models.CASCADE, related_name='history')
    qnum = models.IntegerField()
    rightnum = models.IntegerField()
    end_time = models.DateTimeField(auto_now_add=True)
