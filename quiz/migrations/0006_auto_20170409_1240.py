# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-09 12:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_quizstatus_now_qi'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizstatus',
            name='now_qi',
            field=models.IntegerField(default=0),
        ),
    ]
