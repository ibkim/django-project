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
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'UserManager.views.index'),
    #url(r'^login/$', 'UserManager.views.login_form'),
    url(r'^login/', 'django.contrib.auth.views.login'),
    url(r'^logout/', 'django.contrib.auth.views.logout', {'template_name': 'registration/logout.html',}),
    url(r'^dashboard/$', 'Dashboard.views.index'),
)
