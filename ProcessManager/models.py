# -*- coding: utf-8 -*-

from django.db import models
#from ProjectManager.models import Project
#from UserManager.models import Account

# Create your models here.

class ReqCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(blank=True, null=True, max_length=1000)

    def __unicode__(self):
        return self.name

class WBSCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(blank=True, null=True, max_length=1000)

    def __unicode__(self):
        return self.name

class Requirement(models.Model):
    category = models.ForeignKey(ReqCategory)
    name = models.CharField(max_length=1000)
    description = models.CharField(blank=True, null=True, max_length=1000)
    project = models.ForeignKey('ProjectManager.Project')
    parent = models.IntegerField(blank=True)

    def __unicode__(self):
        return self.name

class WBS(models.Model):
    name = models.CharField(max_length=1000)
    description = models.CharField(blank=True, null=True, max_length=1000)
    category = models.ForeignKey(WBSCategory)
    reqs = models.ManyToManyField(Requirement)
    project = models.ForeignKey('ProjectManager.Project')
    resources = models.ManyToManyField('UserManager.Account')
    start = models.DateField(blank=True, null=True)
    end = models.DateField(blank=True, null=True)
    group = models.IntegerField(blank=True)
    parent = models.IntegerField(blank=True)
    depends = models.CharField(blank=True, null=True, max_length=1000)

    def __unicode__(self):
        return self.name


