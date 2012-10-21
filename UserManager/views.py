# -*- coding: utf-8 -*-

import os
import sys
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Context, loader
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=10)

# Create your views here.
@login_required
def index(request):
    #profile = request.user.get_profile()
    return HttpResponseRedirect('/dashboard/')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
