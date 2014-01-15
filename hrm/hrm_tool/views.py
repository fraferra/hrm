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
        current_user=request.user
        name=return_current_name_object(current_user)[0]
        profile=return_current_name_object(current_user)[1]
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


def logout(request):
    django_logout(request)
    return HttpResponseRedirect('/login/')

def result(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        current_user=request.user
        search = request.GET['search']
       

        results= return_results(search, current_user)
        list_profiles_ordered= return_ordered_list(results)
        list_profiles_ordered['current_user'] = current_user
        list_profiles_ordered['name']=return_current_name_object(current_user)[0]
        list_profiles_ordered['profile']=return_current_name_object(current_user)[1]
    return render(request, 'hrm_tool/result.html', list_profiles_ordered)

#return the profiles that match the query

def return_results(search, current_user):
    result=[]
    list_profiles = return_profiles(current_user)
    for profile in list_profiles:
        for user in profile:
            fields = return_fields(user)
            for value in fields:
                match = re.search(search.lower(), value.lower())
                if match:
                   if user not in result:
                       result.append(user)
    return result

#return a list with the possible searchable profiles, depending on the current user

def return_profiles(current_user):
    if hasattr(current_user, 'seniorvicepresident'):
        profile=SeniorVicePresident.objects.get(user=current_user)
        current_pk=profile.id
        list_profiles=[SeniorVicePresident.objects.all(), SeniorManager.objects.all(), Manager.objects.all(), Employee.objects.all()]
        return list_profiles
    if hasattr(current_user, 'seniormanager'):
        profile=SeniorManager.objects.get(user=current_user)
        current_pk=profile.id
        list_profiles=[ Manager.objects.filter(superior=current_pk), Employee.objects.filter(superior=current_pk)]
        return list_profiles
    if hasattr(current_user, 'manager'):
        profile=Manager.objects.get(user=current_user)
        current_pk=profile.id
        list_profiles=[Employee.objects.filter(superior=current_pk)]
        return list_profiles
    if hasattr(current_user, 'employee'):
        list_profiles=[]
        return list_profiles

#return the fields searchable in every single profile type

def return_fields(user):

    if hasattr(user.user, 'seniorvicepresident'):
        fields= [user.first_name, user.last_name, user.office, user.business_unit.unit  ]
        return fields
    if hasattr(user.user, 'seniormanager'): 
        fields= [user.first_name, user.last_name, user.business_unit.unit  ]
        return fields
    if hasattr(user.user, 'manager'):
        fields= [user.first_name, user.last_name, user.business_unit.unit ]
        return fields
    if hasattr(user.user, 'employee'):
        fields= [user.first_name, user.last_name, user.skill_1, user.skill_2, user.skill_3, user.business_unit.unit ]
        return fields

#return dictionary with results under each category of profile types

def return_ordered_list(results):
    employees =[]
    managers=[]
    seniormanagers=[]
    seniorvicepresidents=[]
    ordered_results={'employees':employees,'managers': managers,'seniormanagers': seniormanagers, 'seniorvicepresidents':seniorvicepresidents}
    users_type=[('seniorvicepresident', seniorvicepresidents),('seniormanager',seniormanagers),('manager',managers),('employee',employees)]
    for result in results:
            for user_type, list in users_type:
                if hasattr(result.user, user_type):
                    list.append(result)
    return ordered_results

#return name and object type for current user

def return_current_name_object(current_user):
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
    list_info=[name,profile]
    return list_info
