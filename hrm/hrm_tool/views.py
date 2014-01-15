# Create your views 
import os
import re
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, render_to_response, redirect
#from hrm_tool.forms import *
from django.http import HttpResponseRedirect, HttpResponse
from hrm_tool.models import *

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as django_logout
from django.template import RequestContext


def home(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        current_pk = request.user.pk
        current_user=request.user
        
        if hasattr(current_user, 'seniorvicepresident'):
            name='seniorvicepresident'
            profile=SeniorVicePresident.objects.get(user=current_user)
        if hasattr(current_user, 'seniormanager'):
            name='seniormanager'
            profile=SeniorManager.objects.get(user=current_user)
        if hasattr(current_user, 'manager'):
            name='manager'
            profile=Manager.objects.get(user=current_user)
        if hasattr(current_user, 'employee'):
            name='employee'
            profile=Employee.objects.get(user=current_user)
    return render(request,'hrm_tool/home.html',{'name':name, 'profile':profile})

def login(request):
    username=password=''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username =username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect('/home/')
            else:
                return HttpResponseRedirect('/login/')
        else:
            return HttpResponseRedirect('hrm_tool/login/')
    return render(request, 'hrm_tool/login.html', {'username':username, 'password':password})


