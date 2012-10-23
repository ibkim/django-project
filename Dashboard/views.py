# -*- coding: utf-8 -*-

import os
import sys
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Context, loader
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django import forms

# Models import
from UserManager.models import Account
from ProjectManager.models import Project
from django.contrib.auth.models import User

# Create your views here.
@login_required
def index(request):
    profile = request.user.get_profile()
    template = loader.get_template('dashboard/index.html')

    # User 의 profile nick 으로 reverse select를 하는데 동명이인이 있다면?
    # 가능하다면 User.username 으로 selecting 을 할 수 있는 방법으로 할 것.
    user = Account.objects.get(nick__exact = profile.nick)
    #projects = user.project_set.all()
    projects = Project.objects.all().order_by('-id')
    #own_projects = Project.objects.filter(owner__exact = request.user).select_related()
    
    #account = projects[0].members.all()
    #print account.all()[0].user.username

    #users = projects[0].members.all().select_related()
    context = Context( {'id': request.user, 'profile': profile, 'projects': projects, } )
    return HttpResponse(template.render(context))
