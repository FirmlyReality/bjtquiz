#-*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.

class MyUserManager(BaseUserManager):

    def create_user(self, uid, password, name, avatar_hd, access_token, expires_in):
        user = self.model(uid = uid)
        user.name = name
        user.avatar_hd = avatar_hd
        user.access_token = access_token
        user.expires_in = expires_in
        user.is_admin = False
        user.set_password(password)
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):

    uid = models.BigIntegerField(unique=True, db_index=True)
    name = models.CharField(max_length=254)
    avatar_hd = models.CharField(max_length=300)
    access_token = models.CharField(max_length=50)
    expires_in = models.BigIntegerField()
    is_admin = models.BooleanField()

    USERNAME_FIELD = "uid"
    objects = MyUserManager()
