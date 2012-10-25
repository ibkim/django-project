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
from models import Project, ProjectForm
from UserManager.models import Account
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt

# Create your views here.
@login_required
def index(request):
    profile = request.user.get_profile()

    if request.method == 'POST':
        f = ProjectForm(request.POST)
        if f.is_valid():
            new_project = f.save(commit=False)
            new_project.wiki = '/project/wiki/' + new_project.unix_name

            user = User.objects.get(username__exact = request.user.username)
            new_project.owner = user

            new_project.save()
            user.project_set.add(new_project)
            f.save_m2m()

            profile = user.get_profile()
            profile.projects.add(new_project)
            profile.save()

            return HttpResponseRedirect('/dashboard/')
    else:
        f = ProjectForm()

    template = loader.get_template('project/create.html')
    context = Context( {'id': request.user, 'profile': profile, 'form': f } )

    return HttpResponse(template.render(context))

