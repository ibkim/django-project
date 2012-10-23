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
    nick = models.CharField(max_length=30)
    mphone = models.CharField(blank=True, null=True, max_length=20)
    ophone = models.CharField(blank=True, null=True, max_length=20)
    org = models.ManyToManyField(Organization, verbose_name=u'조직')
    projects = models.ManyToManyField('ProjectManager.Project', blank=True)

    def __unicode__(self):
        return self.nick

