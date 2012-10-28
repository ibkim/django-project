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
            conf.createRepo([request.user.username,] , project.unix_name)
            conf.addRepo(project.unix_name, [repo_path,])

            members = project.members.all()
            for user in members:
                conf.addUser(project.unix_name, [user.username,])

            result = conf.publish()
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

def test(request, id):
    repo = Repo(settings.GITOLITE_ADMIN, odbt=GitCmdObjectDB)
    repo.config_writer()
    index = repo.index
    
    conf = Gitolite(settings.GITOLITE_ADMIN)
    conf.createRepo(['ibkim2',] , 'django-prj')

    index.add( ['conf/user_repos.conf',] )
    commit = index.commit('add user by django')
    o = repo.remotes.origin
    o.push()

    template = loader.get_template('project/repo.html')
    context = Context( {'repo': id } )

    return HttpResponse(template.render(context))
