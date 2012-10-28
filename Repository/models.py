# -*- coding: utf-8 -*-

from django.db import models
from django import forms
from django.contrib.auth.models import User
 
# Create your models here.
class Repository(models.Model):
    reponame = models.CharField(max_length=255)
    project = models.ForeignKey('ProjectManager.Project', related_name = 'repo-project')
    template_path = models.CharField(blank=True, max_length=255)
    repo_path = models.CharField(blank=True, null=True, max_length=255)
    repo_description = models.CharField(blank=True, max_length=1000)
    creator = models.ForeignKey(User)
    created_date = models.DateField(auto_now_add = True)

    def __unicode__(self):
        return self.reponame.encode('utf-8')

class RepositoryForm(forms.Form):
    name = forms.CharField(label = u'저장소 이름',
                           required = True, max_length = 50)
    description = forms.CharField(label = u'저장소 설명',
                                  widget = forms.Textarea(attrs= {'rows': 5, 'cols': 25}),
                                  required = True, max_length = 1000)
