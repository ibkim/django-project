# -*- coding: utf-8 -*-

# Create your views here.
import os
import sys
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Context, loader
from django.contrib.auth.decorators import login_required
from Repository.models import Repository
from pyproject import settings
from Repository.gitolite import Gitolite
import datetime

from git import *
import copy

from diff2html import parse_from_memory

@login_required
def index(request, id, path=''):
    object = Repository.objects.get(id = id)
    project = object.project

    repo_conf = Gitolite(settings.GITOLITE_ADMIN)

    key_data = repo_conf.getSSHKeys()
    if request.user.username not in key_data:
        repo_user_flag = False
    else:
        repo_user_flag = True

    repo_path = settings.GIT_REPO_ROOT + '/' + object.repo_path + '.git'

    try:
        repo = Repo(repo_path, odbt=GitCmdObjectDB)
    except NoSuchPathError:
        tpl = loader.get_template('error.html')
        ctx = Context( { 'error': u"OOps! Repository path is invalid", } )
        return HttpResponse(tpl.render(ctx))

    # 최초 생성 후 접근일 경우, 참조할 refs 가 없다.
    if 'master' not in repo.heads:
        tpl = loader.get_template('tree.html')
        ctx = Context( { 'HEAD': None, 'is_user': repo_user_flag, 'project': project, 'repo': object, 'dirs': None, 'files': None, } )
        return HttpResponse(tpl.render(ctx))
    try:
        tree = repo.heads.master.commit.tree[path.rstrip('/')]
        #tree = repo.head.commit.tree[path.rstrip('/')]
    except KeyError:
        tree = repo.heads.master.commit.tree

    #print repo.commit('').summary
    trees = map(lambda x: { 'path': os.path.basename(x.path),
                            #'summary': repo.commit(x.blobs[0].hexsha),
                            'link': x.path}, tree.trees)
    files = map(lambda x: { 'path': os.path.basename(x.path),
                            #'summary': repo.commit(x.).summary,
                            'link': x.path}, tree.blobs)

    #path = {'dirname': os.path.dirname(path), 'name': os.path.basename(path)}
    link_paths = {}
    path_param = []
    count = 0
    if path != '':
        path = os.path.normpath(path).split(os.sep)
        link = ''
        for entry in path:
            for item in range(0, len(path) - count):
                if count == 0:
                    link = path[count]
                else:
                    link = link + '/' + path[count]
                link_paths['basename'] = path[count]
                link_paths['link'] = link
                path_param.append(copy.copy(link_paths))
                count = count + 1

    # TODO: this has error, why?
    #blob = repo.heads.homework.commit.tree.blobs[0]
    #ff = blob.data_stream()
    
    tpl = loader.get_template('tree.html')
    ctx = Context( { 'HEAD': repo.head, 'is_user': repo_user_flag, 'project': project, 'repo': object, 'path': path_param, 'repoid': id, 'repo': object, 'dirs': trees, 'files': files, } )

    return HttpResponse(tpl.render(ctx))

class Commit:
    pass

def commits(request, page=1):
    entries = []
    item = Commit()
    item_cnt = 0;
    loop_cnt = 0;
    skip_cnt = 0;
    entry_per_page = 10

    page = int(page)

    if page <= 1:
        skip_cnt = 0
    elif page > 1:
        skip_cnt = (page-1) * entry_per_page
    else:
        skip_cnt = 0

    repo = Repo("/home/ibkim/project/python/mysite", odbt=GitCmdObjectDB)
    commits = repo.iter_commits('homework', max_count = entry_per_page, skip = skip_cnt, author='', grep='')

    commits = map(lambda x: {'hexsha': x.hexsha, 'author': x.author, 'summary': x.summary, 'committed_date': datetime.datetime.fromtimestamp(x.committed_date), 'message': x.message}, commits)

    prev_page_num = page - 1
    next_page_num = page + 1
    if prev_page_num <= 0:
        prev_page_num = 1
    tpl = loader.get_template('commit_list.html')
    ctx = Context( {'refs': repo.heads, 'commits': commits, 'prev_page': prev_page_num, 'next_page': next_page_num,} )
    return HttpResponse(tpl.render(ctx))

def diff(request, sha=''):
    repo = Repo("/home/ibkim/project/python/mysite", odbt=GitCmdObjectDB)

    try:
        commit = repo.commit(sha)
    except BadObject:
        tpl = loader.get_template('error.html')
        ctx = Context( {'error': 'Bad ObjectError',} )
        return HttpResponse(tpl.render(ctx))

    diff = commit.diff( commit.hexsha + '~1', None, True)
    AddDiff = []
    DelDiff = []
    ReDiff = []
    ModDiff = []
    # HTML formatting
    for entry in diff.iter_change_type('M'):
        if entry.deleted_file or entry.new_file or entry.renamed:
            continue
        htmldiff = parse_from_memory(entry.diff, True, True)
        ModDiff.append({'diff': htmldiff,})

    for entry in diff.iter_change_type('A'):
        AddDiff.append(entry)
    for entry in diff.iter_change_type('D'):
        DelDiff.append(entry)
    for entry in diff.iter_change_type('R'):
        ReDiff.append(entry)

    tpl = loader.get_template('diff.html')
    ctx = Context( {'add': AddDiff, 'del': DelDiff, 'rename': ReDiff, 'modify': ModDiff} )
    return HttpResponse(tpl.render(ctx))

def blob(request, id, path=''):
    object = Repository.objects.get(id = id)
    project = object.project

    repo_conf = Gitolite(settings.GITOLITE_ADMIN)

    repo_path = settings.GIT_REPO_ROOT + '/' + object.repo_path + '.git'
    repo = Repo(repo_path, odbt=GitCmdObjectDB)

    git = repo.git
    text = git.show('master:'+path)

    link_paths = {}
    path_param = []
    count = 0
    if path != '':
        path = os.path.normpath(path).split(os.sep)
        link = ''
        for entry in path:
            for item in range(0, len(path) - count):
                if count == 0:
                    link = path[count]
                else:
                    link = link + '/' + path[count]
                link_paths['basename'] = path[count]
                link_paths['link'] = link
                path_param.append(copy.copy(link_paths))
                count = count + 1

    tpl = loader.get_template('blob.html')
    ctx = Context( {'repoid': id, 'reponame': object.reponame, 'path': path_param, 'text': text, } )
    return HttpResponse(tpl.render(ctx))

def blob_old(request, path=''):
    repo = Repo("/home/ibkim/project/pyproject/", odbt=GitCmdObjectDB)

    git = repo.git
    text = git.show('HEAD:'+path)

    link_paths = {}
    path_param = []
    count = 0
    if path != '':
        path = os.path.normpath(path).split(os.sep)
        link = ''
        for entry in path:
            for item in range(0, len(path) - count):
                if count == 0:
                    link = path[count]
                else:
                    link = link + '/' + path[count]
                link_paths['basename'] = path[count]
                link_paths['link'] = link
                path_param.append(copy.copy(link_paths))
                count = count + 1

    tpl = loader.get_template('blob.html')
    ctx = Context( { 'path': path_param, 'text': text, } )
    return HttpResponse(tpl.render(ctx))
    

def makedocs(request, sha=''):
    from docx import *
    relationships = relationshiplist()
    document = newdocument()
    docbody = document.xpath('/w:document/w:body', namespaces=nsprefixes)[0]
    docbody.append(heading('''Welcome to Python's docx module''',1)  )
    docbody.append(heading('Make and edit docx in 200 lines of pure Python',2))
    docbody.append(paragraph('The module was created'))
    for point in ['''COM automation''','''.net or Java''','''Automating OpenOffice or MS Office''']:
        docbody.append(paragraph(point,style='ListNumber'))
    docbody.append(paragraph('''For those of us who prefer something simpler, I made docx.'''))
    docbody.append(heading('Making documents',2))
    #docbody.append(paragraph('''The docx module has the following features:'''))
    
    repo = Repo("/home/ibkim/project/python/mysite", odbt=GitCmdObjectDB)

    try:
        commit = repo.commit(sha)
    except BadObject:
        tpl = loader.get_template('error.html')
        ctx = Context( {'error': 'Bad ObjectError',} )
        return HttpResponse(tpl.render(ctx))

    diff = commit.diff( commit.hexsha + '~1', None, True)
    AddDiff = []
    DelDiff = []
    ReDiff = []
    ModDiff = []
    # HTML formatting
    for entry in diff.iter_change_type('M'):
        if entry.deleted_file or entry.new_file or entry.renamed:
            continue
        htmldiff = parse_from_memory(entry.diff, True, True)
        ModDiff.append({'diff': htmldiff,})
        paratext = [(htmldiff, 'h'),]
        docbody.append(paragraph(paratext))        

    for entry in diff.iter_change_type('A'):
        AddDiff.append(entry)
    for entry in diff.iter_change_type('D'):
        DelDiff.append(entry)
    for entry in diff.iter_change_type('R'):
        ReDiff.append(entry)

    tpl = loader.get_template('diff.html')
    ctx = Context( {'add': AddDiff, 'del': DelDiff, 'rename': ReDiff, 'modify': ModDiff} )

    docbody.append(pagebreak(type='page', orient='portrait'))
    coreprops = coreproperties(title='Python docx demo',subject='A practical example of making docx from Python',creator='Mike MacCana',keywords=['python','Office Open XML','Word'])
    appprops = appproperties()
    contenttypes = contenttypes()
    websettings = websettings()
    wordrelationships = wordrelationships(relationships)
    savedocx(document,coreprops,appprops,contenttypes,websettings,wordrelationships,'diff.docx')
    
    return HttpResponse(tpl.render(ctx))    
