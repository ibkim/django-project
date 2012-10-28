# -*- coding: utf-8 -*-

from django.db import models
from django import forms
from django.forms import ModelForm
from UserManager.models import Account
from Repository.models import Repository
from django.contrib.admin import widgets
from django.contrib.auth.models import User

# Create your models here.
PROCESS_IN_STEP = (
    (u'PLA', u'프로젝트계획/재계획'),
    (u'ANA', u'분석'),
    (u'DES', u'설계'),
    (u'DEV', u'구현'),
    (u'TES', u'시험'),
    (u'DON', u'완료'),
)

class Project(models.Model):
    name         = models.CharField(max_length=255)
    unix_name    = models.CharField(max_length=255, unique=True)
    description  = models.CharField(blank=True, null=True, max_length=1000)
    image_path   = models.CharField(max_length=1000, blank=True, null=True)
    wiki         = models.CharField(max_length=1000, unique=True)
    members      = models.ManyToManyField(User, blank=True, null=True, verbose_name = u'프로젝트 멤버')
    owner        = models.ForeignKey(User, related_name = 'owner')
    repos        = models.ManyToManyField(Repository, blank=True, related_name='project-repo')
    status       = models.CharField(max_length=3, choices = PROCESS_IN_STEP,
                                   default=u'PLA')
    start_date   = models.DateField()
    end_date     = models.DateField()
    created_date = models.DateField(auto_now_add = True)

    def __unicode__(self):
        return u'%s' % self.name

class ProjectForm(ModelForm):
    name        = forms.CharField( widget = forms.TextInput(attrs={'size':40}),
                            help_text = u'원하는 이름으로 프로젝트 명을 작성하세요.' )
    unix_name   = forms.CharField( widget = forms.TextInput(attrs={'size':40}),
                            help_text = u'시스템에서 유일한 unix 이름이어야 합니다. ex) my_my_project-1')
    description = forms.CharField( widget = forms.Textarea(attrs= {'rows': 5, 'cols': 25}))
    #members     = forms.ModelMultipleChoiceField(queryset = User.objects.all())

    start_date  = forms.CharField(widget=forms.TextInput(attrs={'class':'vDateField'}))
    end_date    = forms.CharField(widget=forms.TextInput(attrs={'class':'vDateField'}))

    name.label        = u'프로젝트이름'
    description.label = u'설명'
    start_date.label  = u'시작일'
    end_date.label    = u'종료일'

    class Meta:
        model = Project
        fields = (u'name', u'unix_name', u'description', u'status',
                  u'start_date', u'end_date', )



