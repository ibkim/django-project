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
from Repository.models import Repository, RepositoryForm
from django.views.decorators.csrf import csrf_exempt

#from git import *
from gitolite import *

@csrf_exempt

# Create your views here.
@login_required
def create(request, id):
    project = Project.objects.get(id = id)
    if request.method == 'POST':
        form = RepositoryForm(request.POST)
        if form.is_valid():
            new_repo = Repository(reponame = form.cleaned_data['name'].encode('utf-8'),
                            project = project,
                            creator = request.user,
                            repo_description = form.cleaned_data['description'].encode('utf-8'))

            # Add repository config to gitolite-admin/conf/user_repos.conf
            repo_count = project.repos.all().count()
            repo_path = project.unix_name + '/' + str(repo_count+1)
            conf = Gitolite(settings.GITOLITE_ADMIN)

            conf.lock()
            conf.addRepo(project.unix_name, [repo_path,])

            members = project.members.all()
            for user in members:
                conf.addUser(project.unix_name, [user.username,])

            result = conf.publish()
            conf.unlock()
            if result == False:
                #cleanup all
                conf.rmProject(project.unix_name)
                del new_repo
                template = loader.get_template('error.html')
                context = Context( {'error': u'Failed Create new Repository.' } )
                return HttpResponse(template.render(context))
            new_repo.repo_path = repo_path
            new_repo.save()
            project.repos.add(new_repo)
            project.save()

            return HttpResponseRedirect('/repository/' + str(new_repo.id) + '/')
    else:
        form = RepositoryForm()

    template = loader.get_template('project/repo_form.html')
    context = Context( {'form': form, 'project': project } )

    return HttpResponse(template.render(context))

def delrepo(request, projectid, repoid):
    project = Project.objects.get(id = projectid)
    repo = Repository.objects.get(id = repoid)

    if repo not in project.repos.all():
        template = loader.get_template('error.html')
        context = Context( {'error': repo.reponame + u'은 이미 프로젝트 저장소가 아닙니다. 이상하네요. 이 에러는 발생할 수 없는 에러입니다.' ,} )
        return HttpResponse(template.render(context))

    conf = Gitolite(settings.GITOLITE_ADMIN)
    conf.lock()

    if conf.rmRepo(project.unix_name, [repo.repo_path,]):
        if conf.publish() == False:
            template = loader.get_template('error.html')
            context = Context( {'error': repo.reponame + u'을 석제할 수 없습니다.' ,} )
            conf.unlock()
            return HttpResponse(template.render(context))

    conf.unlock()

    project.repos.remove(repo)
    project.save()
    Repository.delete(repo)

    return HttpResponseRedirect('/project/'+projectid+'/')

def test(request, id):
    repo = Repo(settings.GITOLITE_ADMIN, odbt=GitCmdObjectDB)
    repo.config_writer()
    index = repo.index

    conf = Gitolite(settings.GITOLITE_ADMIN)
    conf.lock()
    conf.createRepo(['ibkim2',] , 'django-prj')

    index.add( ['conf/user_repos.conf',] )
    commit = index.commit('add user by django')
    o = repo.remotes.origin
    o.push()
    conf.unlock()

    template = loader.get_template('project/repo.html')
    context = Context( {'repo': id } )

    return HttpResponse(template.render(context))
