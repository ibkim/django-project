# -*- coding: utf-8 -*-

from django.db import models
from django import forms
from django.forms import ModelForm
from UserManager.models import Account
from Repo.models import Repo
from django.contrib.admin import widgets

# Create your models here.
PROCESS_IN_STEP = (
    ('PLA', '프로젝트계획/재계획'),
    ('ANA', '분석'),
    ('DES', '설계'),
    ('DEV', '구현'),
    ('TES', '시험'),
    ('DON', '완료'),
)

class Project(models.Model):
    name         = models.CharField(max_length=255)
    unix_name    = models.CharField(max_length=255, unique=True)
    description  = models.CharField(blank=True, null=True, max_length=1000)
    image_path   = models.CharField(max_length=1000, blank=True, null=True)
    wiki         = models.CharField(max_length=1000, unique=True)
    members      = models.ManyToManyField(Account, blank=True, verbose_name = '프로젝트 멤버')
    repos        = models.ManyToManyField(Repo, blank=True)
    start_date   = models.DateField()
    end_date     = models.DateField()
    status       = models.CharField(max_length=3, choices = PROCESS_IN_STEP,
                                   default='PLA', verbose_name = '프로젝트 단계')
    created_date = models.DateField()

    def __unicode__(self):
        return u'%s(%s)' % ( self.name, self.unix_name )

class ProjectForm(ModelForm):
    name        = forms.CharField( widget = forms.TextInput(attrs={'size':40}),
                            help_text = '원하는 이름으로 프로젝트 명을 작성하세요.' )
    unix_name   = forms.CharField( widget = forms.TextInput(attrs={'size':40}),
                            help_text = '시스템에서 유일한 unix 이름이어야 합니다. ex) my_my_project-1')
    description = forms.CharField( widget = forms.Textarea(attrs= {'rows': 5, 'cols': 25}))

    start_date  = forms.CharField(widget=forms.TextInput(attrs={'class':'vDateField'}))
    end_date    = forms.CharField(widget=forms.TextInput(attrs={'class':'vDateField'}))

    name.label        = '프로젝트이름'
    description.label = '설명'
    start_date.label  = '시작일'
    end_date.label    = '종료일'

    class Meta:
        model = Project
        fields = ('name', 'unix_name', 'description', 'members', 'status',
                  'start_date', 'end_date', )



