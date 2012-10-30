from django.conf.urls import patterns, include, url
import os

import ProjectManager, ProcessManager, UserManager

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pyproject.views.home', name='home'),
    # url(r'^pyproject/', include('pyproject.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root':SITE_ROOT+'/templates/css'}),
    url(r'^script/(?P<path>.*)$', 'django.views.static.serve', {'document_root':SITE_ROOT+'/templates/scripts'}),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':SITE_ROOT+'/media'}),
    url(r'^$', 'UserManager.views.index'),
    url(r'^account/register/$', 'UserManager.views.register'),
    url(r'^account/setting/$', 'UserManager.views.setting'),
    url(r'^account/setting/sshkey/$', 'UserManager.views.sshkey'),
    url(r'^account/setting/sshkey/add/$', 'UserManager.views.addsshkey'),
    url(r'^account/setting/sshkey/delete/(?P<name>.*)/$', 'UserManager.views.delsshkey'),
    url(r'^login/', 'django.contrib.auth.views.login'),
    url(r'^logout/', 'django.contrib.auth.views.logout', {'template_name': 'registration/logout.html',}),
    url(r'^dashboard/$', 'Dashboard.views.index'),

    url(r'^project/(?P<id>\d+)/$', 'ProjectManager.views.detail'),
    url(r'^project/adduser/(?P<projectid>\d+)/$', 'ProjectManager.views.adduserlist'),
    url(r'^project/adduser/(?P<projectid>\d+)/(?P<userid>\d+)/$', 'ProjectManager.views.adduser'),
    url(r'^project/deluser/(?P<projectid>\d+)/(?P<userid>\d+)/$', 'ProjectManager.views.deluser'),
    url(r'^project/adduser/repository/(?P<projectid>\d+)/(?P<userid>\d+)/$', 'ProjectManager.views.adduser2repo'),
    url(r'^project/deluser/repository/(?P<projectid>\d+)/(?P<userid>\d+)/$', 'ProjectManager.views.deluser2repo'),
    url(r'^repository/(?P<id>\d+)/$', 'Repository.browser.index'),
    url(r'^repository/(?P<id>\d+)/(?P<path>.*)/$', 'Repository.browser.index'),
    url(r'^repository/blob/(?P<id>\d+)/(?P<path>.*)/$', 'Repository.browser.blob'),
    url(r'^repository/new/(?P<id>\d+)/$', 'Repository.views.create'),
    url(r'^repository/del/(?P<projectid>\d+)/(?P<repoid>\d+)/$', 'Repository.views.delrepo'),
    url(r'^project/new/$', 'ProjectManager.views.index'),
)
