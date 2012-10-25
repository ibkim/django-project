# -*- coding: utf-8 -*-

import os
import sys
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Context, loader
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django import forms
from pyproject import settings

# Models import
from UserManager.models import Account
from ProjectManager.models import Project
from django.contrib.auth.models import User

# Create your views here.
@login_required
def index(request):
    profile = request.user.get_profile()
    template = loader.get_template('dashboard/index.html')

    user = User.objects.get(username__exact = request.user.username)
    projects = user.project_set.all().order_by('-id')

    owner_cnt = Project.objects.filter(owner__exact = user).count()
    member_cnt = projects.count()

    if str(profile.avatar.name) is "":
        pic = ""
    else:
        pic = settings.MEDIA_URL+str(profile.avatar.name)

    sidetop = { 'pic': pic, 'owner': owner_cnt, 'member': member_cnt, }

    context = Context( {'id': request.user, 'profile': profile, 'sidetop': sidetop, 'projects': projects, } )
    return HttpResponse(template.render(context))
