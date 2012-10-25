# -*- coding: utf-8 -*-

import os
import sys
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Context, loader
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django import forms
from ProjectManager.models import Project, ProjectForm
from UserManager.models import Account
from pyproject import settings
from django.views.decorators.csrf import csrf_exempt

from git import *
from gitolite import *

@csrf_exempt

# Create your views here.
@login_required
def test(request, id):
    repo = Repo(settings.GITOLITE_ADMIN, odbt=GitCmdObjectDB)
    repo.config_writer()
    index = repo.index
    
    conf = Gitolite(settings.GITOLITE_ADMIN)
    conf.addRepo('ibkim2' , 'myprj3')

    index.add( ['.'] )
    commit = index.commit('add user by django')
    o = repo.remotes.origin
    o.push()

    template = loader.get_template('project/repo.html')
    context = Context( {'repo': id } )

    return HttpResponse(template.render(context))
