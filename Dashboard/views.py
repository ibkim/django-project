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

    user = User.objects.get(username__exact = request.user.username)
    projects = user.project_set.all().order_by('-id')

    context = Context( {'id': request.user, 'profile': profile, 'projects': projects, } )
    return HttpResponse(template.render(context))
