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
from django.forms.models import model_to_dict
import pdb

@csrf_exempt
def Setstatus(request):
    if request.method == 'POST':
        content = request.POST['status']
        discussion = Discussion.objects.get(discussionName = 'Wall')
        status = Status.objects.create(statusAuthor = request.user,statusDiscussion = discussion, statusContent= content,statusDelete =0)
        model = model_to_dict(status)
        data = json.dumps({'status':model})
        return HttpResponse(data, content_type="application/json")

@csrf_exempt
def Getstatus(request):
    if request.method == "POST":
        a = []
        b = []
        discussion = Discussion.objects.get(discussionName = "Wall")
        statuss  = Status.objects.filter(statusDiscussion = discussion,statusDelete = False)  #list status
        for status in statuss:
            y = [like.as_json() for like in LikeStatus.objects.filter(likeStatus = status,likeContent=1)]
            likest= str(json.dumps({'likeStatus':y}))                                     # list like for each status
            commentStatuss = CommentStatus.objects.filter(commentStatus = status)
            for commentS in commentStatuss:
                x = [like.as_json() for like in LikeComment.objects.filter(likeComment=commentS,likeContent=1)]
                x = json.dumps({'likecomment': x})
                likecmt = str(x)
                cmt = str(json.dumps({'commentContent':commentS.as_json()}))
                comment = dict(comment = cmt , likecomment = likecmt,)
                a.append(comment)
            comments = str(json.dumps({'commentStatus':a}))                             #list comment for each status
            a = []
            st = dict(
                      status = str(json.dumps(status.as_json())),
                      comments = comments,
                      likestatus = likest,
                      )
            b.append(st)
        data = json.dumps({'statuss':b,})
        
        return HttpResponse(data, content_type="application/json")

@csrf_exempt 
def Setcomment(request):
    if request.method == "POST":
        statusID = request.POST["statusID"]
        content = request.POST["comment"]
        if content != "":
            status = Status.objects.get(statusID = statusID)
            comment = CommentStatus.objects.create(commentAuthor = request.user, commentStatus = status,commentContent = content,commentDelete = False )
            comment.save()
            a = comment.as_json()
            data = json.dumps({'commentContent':a,})
            
        else:
            data = "error"
        return HttpResponse(data, content_type="application/json")
@csrf_exempt 
def Setlike(request):
    if request.method =="POST":
        if request.POST["statusID"]:
            statusID = request.POST["statusID"]
            status = Status.objects.get(statusID=statusID)
            likes = LikeStatus.objects.filter(likeStatus = statusID)
            for l in likes:
                if l.likeAuthor == request.user:
                    if l.likeContent == 1:
                        data = "error"
                        return HttpResponse(data)
                    else:
                        l.likeContent = 1
                        l.save()
                        data = "success"
                        return HttpResponse(data)
            like = LikeStatus.objects.create(likeAuthor = request.user,likeStatus = status, likeContent = 1)
            like.save()
            a = like.as_json()
            data = json.dumps({'commentContent':a,})
            return HttpResponse(data, content_type="application/json")
        else:
            data = "error"
    return HttpResponse(data)      
@csrf_exempt 
def Removelike(request):
    if request.method =="POST":
        if request.POST["statusID"]:
            statusID = request.POST["statusID"]
            status = Status.objects.get(statusID=statusID)
            like = LikeStatus.objects.get(likeAuthor = request.user,likeStatus = status)
            like.likeContent = 0
            like.save()
            data = "success"
            return HttpResponse(data)
    elif request.method =="GET":
        if request.GET["statusID"]:
            statusID = request.GET["statusID"]
            status = Status.objects.get(statusID=statusID)
            like = LikeStatus.objects.get(likeAuthor = request.user,likeStatus = status)
            like.likeContent = 0
            like.save()
            data = "success"
            return HttpResponse(data)
    else:
            data = "error"
    return HttpResponse(data) 
            