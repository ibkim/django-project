# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django import forms
# Create your models here.

class Organization(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name

class Account(models.Model):
    user = models.OneToOneField(User, unique=True)
    avatar = models.ImageField(u"Profile Pic", upload_to="avatars/", blank=True, null=True, max_length=1000)
    nick = models.CharField(max_length=30)
    mphone = models.CharField(blank=True, null=True, max_length=20)
    ophone = models.CharField(blank=True, null=True, max_length=20)
    org = models.ManyToManyField(Organization, verbose_name=u'조직')
    projects = models.ManyToManyField('ProjectManager.Project', blank=True)

    def __unicode__(self):
        return self.nick


class AccountForm(forms.Form):
    username = forms.CharField(label = u'사용자 계정 이름', required = True, max_length = 50)
    avatar = forms.ImageField(required = False)
    email = forms.EmailField(required = True)
    pass1 = forms.CharField(label = u'Password', required = True, max_length=10)
    pass2 = forms.CharField(label = u'Password 재입력', required = True, max_length=10)
    nick = forms.CharField(label = u'사용자 실명', required = True, initial = u'홍길동',  max_length=50)
    org = forms.ModelChoiceField(label = u'부서', queryset = Organization.objects.all(), empty_label="-------------", required = True)

