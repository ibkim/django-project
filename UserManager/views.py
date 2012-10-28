# -*- coding: utf-8 -*-

import os
import sys
from os.path import join as pjoin
from PIL import Image as PImage

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Context, loader
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django import forms
from django.contrib.auth.models import User
from ProjectManager.models import Project, ProjectForm
from UserManager.models import Organization, Account, AccountForm, AddKeyForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from pyproject import settings
from Repository.gitolite import Gitolite

@csrf_exempt

def register(request):
    if request.method == 'POST':
        form = AccountForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.create(username = form.cleaned_data['username'],
                                       email = form.cleaned_data['email'],
                                       password = make_password(form.cleaned_data['pass1']),
                                       is_active = True)
            profile = Account(user = user,
                              nick = form.cleaned_data['nick'],
                              avatar = form.cleaned_data['avatar'])
            profile.save()
            profile.org.add(form.cleaned_data['org'])
            user.save()

            image_path = pjoin(settings.MEDIA_ROOT, str(profile.avatar))
            image = PImage.open(image_path)
            image.thumbnail((160,160), PImage.ANTIALIAS)
            image.save(image_path, "PNG")

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

def setting(request):
    template = loader.get_template('account/setting.html')
    context = Context( {'form': None, } )

    return HttpResponse(template.render(context))

def sshkey(request):
    conf = Gitolite(settings.GITOLITE_ADMIN)
    keys = conf.getSSHKeys()

    try:
        mykeys = keys[request.user.username]
    except KeyError:
        mykeys = []
    
    template = loader.get_template('account/sshkey.html')
    context = Context( {'sshkey': mykeys, } )

    return HttpResponse(template.render(context))

@csrf_exempt
def addsshkey(request):
    if request.method == 'POST':
        form = AddKeyForm(request.POST)
        if form.is_valid():
            conf = Gitolite(settings.GITOLITE_ADMIN)
            key_value = form.cleaned_data['key']
            key_name = form.cleaned_data['name'].encode('utf-8')

            conf.addSSHKey(request.user.username, key_name, key_value)
            if conf.publish() == False:
                template = loader.get_template('error.html')
                context = Context( {'error': u'Cannot Publish your SSH key', } )
                return HttpResponse(template.render(context))

            HttpResponseRedirect('/account/setting/sshkey/')
    else:
        form = AddKeyForm()

    template = loader.get_template('account/addsshkey.html')
    context = Context( {'form': form, } )

    return HttpResponse(template.render(context))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

