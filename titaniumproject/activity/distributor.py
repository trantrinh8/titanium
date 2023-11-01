# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect,HttpResponse
# from public.forms import*
from titanium.models import*
from django.db.models import Count
# from public.base import*
# from bson.son import SON
from django.utils import simplejson as json
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import pdb

@csrf_exempt   
def Getmyactivity(request):
    if request.method == "POST":
        myactivity = [l.as_json() for l in Answer.objects.filter(answerUser=request.user).order_by('-answerCreated')]
        data = json.dumps({"myactivity":myactivity})
        return HttpResponse(data, mimetype="application/json")