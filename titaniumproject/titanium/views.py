# -*- coding: utf-8 -*-
# Create your views here.
from django.shortcuts import render
from django.core.context_processors import csrf, request
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect,HttpResponse
from titanium.models import *
import random
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
import time

#@csrf_exempt 
#def Signup(request):
#    if request.method == "POST":
 #       email = request.POST['email']
 #       password = request.POST['password']
#        firstname = request.POST['firstname']
#        lastname = request.POST['lastname']
#        sameuser = User.objects.filter(first_name=firstname,last_name=lastname)
#        id = len(sameuser)+1
#        username = lastname+'.'+firstname+'.'+str(id)
#        gender = request.POST['gender']
#        
#        birthday = request.POST['birthday'][0:9]
 #       
 #       user = User.objects.create(username=username,email = email,password=password,first_name = firstname,last_name = lastname)
  #      user.save()
 #       authorization = Authorization.objects.get(authorizationID = 1)
 #       account = Account.objects.create(accountUser = user,accountAuthorization = authorization,accountGender= gender,accountBirthday =birthday )
 #       account.save()
 #       course = Course.objects.get(courseName = "Free course")
 #       type = Type.objects.get(typeKey = "students")
 #       myclass = Classroom.objects.create(classroomUser=user,classroomCourse=course,classroomRole=type,classroomActive=True)
 #       myclass.save()
        # gửi mail
        #subject     = u'[EE Learning] Thông tin đăng ký tài khoản English - uit'
       # from_email  = 'englishuit@gmail.com'
       # to          = user.email
       # text_content = 'abc'
      #  html_content = u'<p>Hi %s!<br />Thank you for registering an account at english - UIT. </br>Register content:<br />Email: <a href="#">%s</a><br />Name: %s %s<br />The registration process is not yet complete. Please complete additional information.</br>Thank you!</br>EE learning</p>' % (user.username,user.email,user.first_name,user.last_name)
      #  msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
       # msg.attach_alternative(html_content, "text/html")
     #   msg.send()
  #      a=True
   #     data = json.dumps({'messgae': a})
    #    return HttpResponse(data, content_type="application/json")

@csrf_exempt 
def Signup(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        sameuser = User.objects.filter(first_name=firstname,last_name=lastname)
        id = len(sameuser)+1
        username = lastname+'.'+firstname+'.'+str(id)
        gender = request.POST['gender']
        
        birthday = request.POST['birthday'][0:9]
        
        user = User.objects.create_user(username,email,password)
        user.first_name = firstname
		user.last_name = lastname
		user.save()
        authorization = Authorization.objects.get(authorizationID = 1)
        account = Account.objects.create(accountUser = user,accountAuthorization = authorization,accountGender= gender,accountBirthday =birthday )
        account.save()
        course = Course.objects.get(courseName = "Free course")
        type = Type.objects.get(typeKey = "students")
        myclass = Classroom.objects.create(classroomUser=user,classroomCourse=course,classroomRole=type,classroomActive=True)
        myclass.save()
        # gửi mail
        #subject     = u'[EE Learning] Thông tin đăng ký tài khoản English - uit'
       # from_email  = 'englishuit@gmail.com'
       # to          = user.email
       # text_content = 'abc'
      #  html_content = u'<p>Hi %s!<br />Thank you for registering an account at english - UIT. </br>Register content:<br />Email: <a href="#">%s</a><br />Name: %s %s<br />The registration process is not yet complete. Please complete additional information.</br>Thank you!</br>EE learning</p>' % (user.username,user.email,user.first_name,user.last_name)
      #  msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
       # msg.attach_alternative(html_content, "text/html")
     #   msg.send()
        a=True
        data = json.dumps({'messgae': a})
        return HttpResponse(data, content_type="application/json")
@csrf_exempt 
@login_required(login_url='login')
def Index(request):
    return render(request,'titanium/index.html')

@csrf_exempt 
@login_required(login_url='login')
def Base(request):
    account = Account.objects.get(accountUser = request.user)
    authorization = account.accountAuthorization.authorizationID
    
    return render(request,'titanium/base.html',{'authorization':authorization})
    
# @csrf_exempt 
# @login_required(login_url='login')
# def Course(request):
#     return render(request,'titanium/course.html')

@csrf_exempt 
@login_required(login_url='login')
def CourseView(request):
    return render(request,'titanium/course.html')

@csrf_exempt 
@login_required(login_url='login')
def MyProfile(request):
    return render(request,'titanium/myprofile.html')

def error404(request,error):
    return render(request,'titanium/404.html')

@csrf_exempt 
@login_required(login_url='login')
def helps(request):
    return render(request,'titanium/helps.html')

@csrf_exempt 
@login_required(login_url='login')
def registerschool(request):
    return render(request,'titanium/registerschool.html')