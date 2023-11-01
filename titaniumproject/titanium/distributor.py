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
from titanium.loggers import MyDbLogHandler
import logging
import pdb

logger = logging.getLogger(__name__)

@csrf_exempt
def TestEmail(request):
    if request.method == 'POST':
        users = User.objects.all()
        message = True
        for user in users:
            if user.email == request.POST['email']:
                message = False
        data = json.dumps({'message':message})
#          request.GET['usr']
        return HttpResponse(data, content_type="application/json")
    
@csrf_exempt
def GetUser(request):
#     pdb.set_trace()
#     print request.method
#     pdb.set_trace()
    
    if request.method == 'POST':
        acc = SimpleAccount(request.user)        
        data = json.dumps(acc)
#          request.GET['usr']
        return HttpResponse(data, content_type="application/json")
    elif request.method == 'GET':
        
        acc = SimpleAccount(request.user)        
        data = json.dumps(acc)
#          request.GET['usr']
        return HttpResponse(data, content_type="application/json")
@csrf_exempt
def GetCourse(request):
    
    if request.method == 'GET':
        allLevel =  [l.as_json() for l in Level.objects.all()]
        allClass = [c.classroomCourse for c in Classroom.objects.filter(classroomUser=request.GET['usr'])]
        allUnit = [u.as_json() for u in Unit.objects.filter(unitCourse__in = allClass,unitDelete = False)]
        allSkill = [u.as_json() for u in Type.objects.filter(typeDelete = False)]
        allCourse = [u.as_json() for u in Course.objects.filter(courseDelete = False)]
        data = json.dumps({'allLevel':allLevel,'allUnit':allUnit,'allSkill':allSkill,'allCourse':allCourse})
        
        return HttpResponse(data, content_type="application/json")
    elif request.method == 'POST':     
        allLevel =  [l.as_json() for l in Level.objects.all()]
        allClass = [c.classroomCourse for c in Classroom.objects.filter(classroomUser=request.POST['usr'])]
        allUnit = [u.as_json() for u in Unit.objects.filter(unitCourse__in = allClass,unitDelete = False)]
        allSkill = [u.as_json() for u in Type.objects.filter(typeDelete = False)]
        allCourse = [u.as_json() for u in Course.objects.filter(courseDelete = False)]
        data = json.dumps({'allLevel':allLevel,'allUnit':allUnit,'allSkill':allSkill,'allCourse':allCourse})
        return HttpResponse(data, content_type="application/json")


@csrf_exempt
def GetMyClass(request):
    if request.method =="POST":
        a=[]
        b=[]
        classrooms = Classroom.objects.filter(classroomUser = request.user)
        for cl in classrooms:
            a=[]
            units = Unit.objects.filter(unitCourse = cl.classroomCourse,unitDelete = False)
            for unt in units:
                
                question = [qs.as_json() for qs in Question.objects.filter(questionUnit = unt)]
                x = json.dumps({"unit":unt.as_json(),"question":question})
                a.append(dict(unit = str(x)))
            y = json.dumps({"classes": cl.as_json(),"unit":a})
            b.append(dict(classes =str(y)))
        data = json.dumps({"myclass":b})
        return HttpResponse(data, content_type="application/json")
    if request.method =="GET":
        a=[]
        b=[]
        classrooms = Classroom.objects.filter(classroomUser = request.user)
        for cl in classrooms:
            a=[]
            units = Unit.objects.filter(unitCourse = cl.classroomCourse,unitDelete = False)
            for unt in units:
                
                question = [qs.as_json() for qs in Question.objects.filter(questionUnit = unt)]
                x = json.dumps({"unit":unt.as_json(),"question":question})
                a.append(dict(unit = str(x)))
            y = json.dumps({"classes": cl.as_json(),"unit":a})
            b.append(dict(classes =str(y)))
        data = json.dumps({"myclass":b})
        return HttpResponse(data, content_type="application/json")

#create class
@csrf_exempt
def SetCourse(request):
    if request.method == "POST":
        levelCourse = request.POST["levelcourse"]
        courseName = request.POST["courseName"]
        courseDescription = request.POST["courseDescription"]
        level = Level.objects.get(levelName = levelCourse)
        course = Course.objects.create(courseAuthor=request.user,courseLevel = level,courseName = courseName,courseDescription=courseDescription,courseDelete = False)
        
        type = Type.objects.get(typeKey = 'teachers')
        classroom = Classroom.objects.create(classroomUser = request.user,classroomCourse = course, classroomRole = type,classroomActive = True)
        course.save()
        classroom.save()
        data = json.dumps({'course':course.as_json()})
        return HttpResponse(data, mimetype="application/json")
@csrf_exempt
def SetQuestion(request):
    if request.method == "POST":
       # pdb.set_trace()
        #post=json.loads(request.POST)
        #print request.POST
        unit = request.POST['unit']
        skill = request.POST['skill']
        type = request.POST['type']
        title = request.POST['title']
        contents = request.POST['questionContents']
        questionUnit = Unit.objects.get(unitName= unit)
        questionType = Type.objects.get(typeName= type)
        questionSkill = Type.objects.get(typeName= skill)
        question = Question.objects.create(questionUnit = questionUnit,questionAuthor = request.user, questionType = questionType,questionSkill=questionSkill,questionTitle= title,questionContents = contents,questionDelete = False)
        question.save()
        qs = question.as_json()
        data = json.dumps({'question':qs})
        return HttpResponse(data, mimetype="application/json")
    elif request.method == "GET":
        unit = request.GET['unit']
        skill = request.GET['skill']
        type = request.GET['type']
        data = json.dumps({'unit':unit,'skill':skill,'type':type})
        return HttpResponse(data, content_type="application/json")
@csrf_exempt
def GetQuestion(request):
    if request.method == "POST":
        question = Question.objects.get(questionID = request.POST['id'])
        qs = question.as_json()
        #question = json.loads(question.questionContents)
        
        data = json.dumps({'question':qs})
        return HttpResponse(data, content_type="application/json")
    elif request.method == "GET":
        question = Question.objects.get(questionID = request.GET['id'])
        qs = question.as_json()
        question = json.loads(question.questionContents)
        data = json.dumps({'question':qs})
        return HttpResponse(data, content_type="application/json")
@csrf_exempt
def SetUnit(request):
    if request.method == "POST":
       # pdb.set_trace()
        #post=json.loads(request.POST)
        #print request.POST
        unitcourse = request.POST['unitcourse']
        unittype = request.POST['unittype']
        name = request.POST['name']
        description = request.POST['description']
        unitcourse = Course.objects.get(courseName= unitcourse)
        unittype = Type.objects.get(typeName= unittype)
        unit = Unit.objects.create(unitAuthor=request.user, unitCourse=unitcourse, unitType = unittype, unitName = name, unitDescription = description, unitDelete =False  )
        unit.save()
        un = unit.as_json()
        data = json.dumps({'unit':un})
        return HttpResponse(data, mimetype="application/json")
    elif request.method == "GET":
        unitcourse = request.GET['unitcourse']
        unittype = request.GET['unittype']
        name = request.GET['name']
        description = request.GET['description']
        unitcourse = Course.objects.get(courseName= unitcourse)
        unittype = Type.objects.get(typeName= unittype)
        unit = Unit.objects.create(unitAuthor=request.user, unitCourse=unitcourse, unitType = unittype, unitName = name, unitDescription = description, unitDelete =False  )
        unit.save()
        un = unit.as_json()
        data = json.dumps({'unit':un})
        return HttpResponse(data, content_type="application/json")
@csrf_exempt
def GetQuestionUnit(request):
    if request.method == "POST":
        unit_id = request.POST['unitid']
        unit = Unit.objects.get(unitID = unit_id)
        questions = [u.as_json() for u in Question.objects.filter(questionUnit = unit)]
        data = json.dumps({'questions':questions})
        return HttpResponse(data, content_type="application/json")
    if request.method == "GET":
        unit_id = request.GET['unitid']
        unit = Unit.objects.get(unitID = unit_id)
        questions = [u.as_json() for u in Question.objects.filter(questionUnit = unit)]
        data = json.dumps({'questions':questions})
        return HttpResponse(data, content_type="application/json")

@csrf_exempt
def setAnswer(request):
    if request.method == "POST":
        answerQuestion = Question.objects.get(questionID = request.POST['questionID'])
        answerContent = request.POST['answerContent']
        answerScore = request.POST['answerScore']
        answer = Answer.objects.create(answerUser=request.user,answerQuestion = answerQuestion,answerContent = answerContent,answerScore=answerScore)
        answer.save()
        data = []
        return HttpResponse(data, content_type="application/json")
    
@csrf_exempt
def getFullUser(request):
    if request.method == "POST":
        user = FullAccount(request.user)
        data = json.dumps({'fulluser':user})
        return HttpResponse(data, content_type="application/json")

@csrf_exempt
def getAlluniversity(request):
    if request.method == "POST":
        Alluniversity = [uns.as_json() for uns in University.objects.all()]
        data = json.dumps({'Alluniversity':Alluniversity})
        return HttpResponse(data, content_type="application/json")