# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=255)
    unix_name = models.CharField(max_length=255, unique=True)
    description = models.CharField(blank=True, null=True, max_length=1000)
    image_url = models.URLField(blank=True, null=True)
    wiki = models.CharField(max_length=1000, unique=True)
    members = models.ManyToManyField('UserManager.Account', blank=True)
    repos = models.ManyToManyField('Repo.Repo', blank=True)
    created_date = models.DateField()

    def __unicode__(self):
        return u'%s(%s)' % ( self.name, self.unix_name )

