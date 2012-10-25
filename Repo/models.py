# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.
class Repo(models.Model):
    name = models.CharField(max_length=255)
    project_unix = models.ManyToManyField('ProjectManager.Project')
    template_path = models.CharField(blank=True, max_length=255)
    repo_path = models.CharField(blank=True, unique=True, max_length=255)
    description = models.CharField(blank=True, max_length=1000)
    creator = models.ForeignKey('UserManager.Account')
    created_date = models.DateField(auto_now_add = True)

    def __unicode__(self):
        return u'%s' % (self.name,)
