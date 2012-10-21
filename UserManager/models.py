# -*- coding: utf-8 -*-

from django.db import models
#from ProjectManager.models import Project

# Create your models here.

class Organization(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name

class Account(models.Model):
    name = models.CharField(max_length=30)
    nick = models.CharField(max_length=30)
    email = models.EmailField()
    mphone = models.CharField(blank=True, null=True, max_length=20)
    ophone = models.CharField(blank=True, null=True, max_length=20)
    created_date = models.DateField()
    org = models.ManyToManyField(Organization, verbose_name=u'조직')
    projects = models.ManyToManyField('ProjectManager.Project', blank=True)

    def __unicode__(self):
        return self.name

