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
def Uploadfile(request):
    
    if request.FILES:
        type ="other"
        file_upload = request.FILES['file']
        if ".jpg" in file_upload.name or ".png" in file_upload.name or ".jpeg" in file_upload.name or ".bmp" in file_upload.name or ".gif" in file_upload.name:
            type = "image"
        elif ".pdf" in file_upload.name:
            type = "pdf"
        elif ".mp3" in file_upload.name:
            type = "mp3"
        file = File.objects.create( 
                                   fileFile = file_upload,
                                   fileName = file_upload.name,
                                   fileCategory = type,
                                   fileUser = request.user
                                   )
        file.save()
        a = file.as_json()
        data = json.dumps({'file':a})
        return HttpResponse(data, mimetype="application/json")
    else:
        return HttpResponse('no file')

@csrf_exempt   
def Getmyfile(request):
    if request.method == "POST":
        files = [l.as_json() for l in File.objects.filter(fileUser=request.user)]
        data = json.dumps({"files":files})
        return HttpResponse(data, mimetype="application/json")
    
@csrf_exempt   
def Setavatar(request):
    if request.method =="POST":
        file = File.objects.get(fileID =request.POST['fileID'] )
        acc = Account.objects.get(accountUser=request.user)
        acc.accountAvatar = file
        acc.save()
        account = SimpleAccount(request.user)
        data = json.dumps({"account":account})
        return HttpResponse(data, mimetype="application/json")
        