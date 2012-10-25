# -*- coding: utf-8 -*-

import os
import sys
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Context, loader
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django import forms
from django.contrib.auth.models import User
from ProjectManager.models import Project, ProjectForm
from UserManager.models import Organization, Account, AccountForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
@csrf_exempt

def register(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            user = User.objects.create(username = form.cleaned_data['username'],
                                       email = form.cleaned_data['email'],
                                       password = make_password(form.cleaned_data['pass1']),
                                       is_active = True)
            profile = Account(user = user,
                              nick = form.cleaned_data['nick'])
            profile.save()
            profile.org.add(form.cleaned_data['org'])
            user.save()

            login_user = authenticate(username = user.username,
                                      password = form.cleaned_data['pass1'])
            if login_user is not None:
                if user.is_active:
                    login(request, login_user);
                    HttpResponseRedirect('/dashboard/')
                else:
                    template = loader.get_template('error.html')
                    context = Context( {'error': u'Failed User Login.' } )
                    return HttpResponse(template.render(context))
            else:
                template = loader.get_template('error.html')
                context = Context( {'error': u'Invalid Login' } )
                return HttpResponse(template.render(context))

            return HttpResponseRedirect('/dashboard/')
    else:
        form = AccountForm()

    template = loader.get_template('registration/register.html')
    context = Context( {'form': form } )

    return HttpResponse(template.render(context))

@login_required
def index(request):
    #profile = request.user.get_profile()
    return HttpResponseRedirect('/dashboard/')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

