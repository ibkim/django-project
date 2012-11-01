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
from pyproject import settings
from django.views.decorators.csrf import csrf_exempt
from Repository.gitolite import Gitolite
import copy

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
            
            conf = Gitolite(settings.GITOLITE_ADMIN)
            conf.lock()
            conf.createRepo([request.user.username,] , new_project.unix_name)
            result = conf.publish()
            conf.unlock()
            if result == False:
                template = loader.get_template('error.html')
                context = Context( {'error': u'프로젝트의 저장소를 초기화하는데 실패했습니다.' ,} )
                return HttpResponse(template.render(context))

            return HttpResponseRedirect('/dashboard/')
    else:
        f = ProjectForm()

    template = loader.get_template('project/create.html')
    context = Context( {'id': request.user, 'profile': profile, 'form': f } )

    return HttpResponse(template.render(context))

def detail(request, id):
    project = Project.objects.get(id = id)
    members = project.members.all()
    conf = Gitolite(settings.GITOLITE_ADMIN)

    users = []
    user = {}
    for entry in members:
        user['id'] = entry.id
        user['username'] = entry.username
        user['nick'] = entry.get_profile().nick
        user['avatar'] = entry.get_profile().avatar
        user['pushable'] = conf.isThereUser(project.unix_name, entry.username)
        users.append(copy.copy(user))

    media_root = settings.MEDIA_URL

    template = loader.get_template('project/detail.html')
    context = Context( {'project': project, 'users': users, 'media': media_root } )

    return HttpResponse(template.render(context))

def adduserlist(request, projectid):
    project = Project.objects.get(id = projectid)
    users = User.objects.all()
    members = project.members.all()

    template = loader.get_template('project/adduserlist.html')
    context = Context( {'project': project, 'users': users, 'members': members, 'media': settings.MEDIA_URL} )

    return HttpResponse(template.render(context))

def adduser(request, projectid, userid):
    project = Project.objects.get(id = projectid)
    user = User.objects.get(id = userid)

    if user in project.members.all():
        template = loader.get_template('error.html')
        context = Context( {'error': user.username + u'은 이미 프로젝트 멤버로 등록되어 있습니다.' ,} )
        return HttpResponse(template.render(context))
    else:
        project.members.add(user)
        project.save()

    return HttpResponseRedirect('/project/'+projectid+'/')

def deluser(request, projectid, userid):
    project = Project.objects.get(id = projectid)
    user = User.objects.get(id = userid)

    if user not in project.members.all():
        template = loader.get_template('error.html')
        context = Context( {'error': user.username + u'은 이미 프로젝트 멤버가 아닙니다. 이상하네요. 이 에러는 발생할 수 없는 에러입니다.' ,} )
        return HttpResponse(template.render(context))
    else:
        project.members.remove(user)
        project.save()

    # 저장소에서 push 권한 빼기
    conf = Gitolite(settings.GITOLITE_ADMIN)
    conf.lock()

    conf.rmUser(project.unix_name, [user.username,])

    if conf.publish() == False:
        template = loader.get_template('error.html')
        context = Context( {'error': user.username + u'을 프로젝트 저장소에 추가할 수 없습니다.' ,} )
        conf.unlock()
        return HttpResponse(template.render(context))

    conf.unlock()

    return HttpResponseRedirect('/project/'+projectid+'/')


def adduser2repo(request, projectid, userid):
    project = Project.objects.get(id = projectid)
    user = User.objects.get(id = userid)

    conf = Gitolite(settings.GITOLITE_ADMIN)
    conf.lock()

    conf.addUser(project.unix_name, [user.username,])

    if conf.publish() == False:
        template = loader.get_template('error.html')
        context = Context( {'error': user.username + u'을 프로젝트 저장소에 추가할 수 없습니다.' ,} )
        conf.unlock()
        return HttpResponse(template.render(context))

    conf.unlock()
    return HttpResponseRedirect('/project/'+projectid+'/')

def deluser2repo(request, projectid, userid):
    project = Project.objects.get(id = projectid)
    user = User.objects.get(id = userid)

    conf = Gitolite(settings.GITOLITE_ADMIN)
    conf.lock()

    conf.rmUser(project.unix_name, [user.username,])

    if conf.publish() == False:
        template = loader.get_template('error.html')
        context = Context( {'error': user.username + u'을 프로젝트 저장소에 추가할 수 없습니다.' ,} )
        conf.unlock()
        return HttpResponse(template.render(context))

    conf.unlock()
    return HttpResponseRedirect('/project/'+projectid+'/')
