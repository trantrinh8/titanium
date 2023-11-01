# -*- coding: utf-8 -*-

from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from titanium.forms import *
from titanium.models import *
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def LoginView(request):
    message =''
    if request.method == 'POST':
        message = "Incorrect password or email! Please check again! Thank you!"
        email = request.POST['email']
        password = request.POST['password']
        checkemail = ContactForm(request.POST)
        if checkemail.is_valid():
            username = User.objects.get(email = email).username
            user = authenticate(username =username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
    #                 request.session['email']=email
                    if 'next' in request.REQUEST:
                        return HttpResponseRedirect(request.REQUEST['next'])
                    else :
                        return HttpResponseRedirect(reverse('base'))
    c={'contact_form': ContactForm(),'message':message}
    return render(request, 'titanium/login.html',c)
@csrf_exempt
def LogoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


    