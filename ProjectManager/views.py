# -*- coding: utf-8 -*-

import os
import sys
import datetime
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Context, loader
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
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
            new_project.created_date = datetime.datetime.now()
            new_project.wiki = '/project/wiki/' + new_project.unix_name
            new_project.owner = request.user
            account = Account.objects.get(nick = profile.nick)

            # save 한 뒤 manytomany field를 add 해야 한다.
            # db에 저장된 뒤 primary key 가 존재해야만 m2m field를 따로 저장 가능
            new_project.save()
            new_project.members.add(account)
            new_project.save()
            f.save_m2m()
            return HttpResponseRedirect('/dashboard/')
    else:
        f = ProjectForm()

    template = loader.get_template('project/create.html')
    context = Context( {'id': request.user, 'profile': profile, 'form': f } )

    return HttpResponse(template.render(context))

