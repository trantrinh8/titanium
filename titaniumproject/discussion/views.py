# Create your views here.
# -*- coding: utf-8 -*-
# Create your views here.
from django.shortcuts import render
from django.core.context_processors import csrf, request
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from titanium.models import *

@csrf_exempt 
@login_required(login_url='login')
def DiscussionViews(request):
    return render(request,'discussion/discussion.html')