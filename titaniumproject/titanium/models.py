# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from titaniumproject import settings
# from xmlrpclib import datetime
from django.utils import timezone
from django.utils import simplejson as json
# Create your models here.


class SystemErrorLog(models.Model):
    level = models.CharField(max_length=200)
    message = models.TextField()
    request = models.TextField(blank=True )
    ipuser = models.CharField(max_length=100,blank=True )
    timestamp = models.DateTimeField(auto_now_add=True)
    
def UserDict(user):    
    return dict(
                id =user.id , 
                username =user.username, 
                first_name=user.first_name, 
                last_name=user.last_name, 
                is_active=user.is_active, 
                is_superuser=user.is_superuser, 
                is_staff=user.is_staff, 
                last_login=user.last_login.isoformat(), 
                email=user.email, 
                date_joined=user.date_joined.isoformat()
                )

class File(models.Model):
        Choices = (
                   ('pdf','pdf'),
                   ('mp3','mp3'),
                   ('image','image'),
                   ('other','other'),
                   )
        fileID = models.AutoField(primary_key=True)
        fileFile = models.FileField(upload_to = settings.MEDIA_ROOT)
        fileName = models.CharField(max_length = 200)
        fileCategory = models.CharField(choices = Choices, max_length = 20)
        fileUser = models.ForeignKey(User)
        fileDelete = models.BooleanField(default=False)
        fileCreated = models.DateTimeField(auto_now_add=True)
        def __unicode__(self):  # Python 3: def __str__(self):
            return self.fileName
        class Meta:
            ordering = ['fileName']
        def as_json(self):
            return dict(
                fileID=self.fileID, 
                fileType = self.fileCategory,
                fileName = self.fileName
                        )
            
            
class Authorization(models.Model):
    authorizationID = models.AutoField(primary_key = True)    
    authorizationName = models.TextField()
    authorizationDescription = models.TextField()
    authorizationDelete = models.BooleanField(default=False)
    authorizationCreated = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.authorizationName
    
class Role(models.Model):
    roleID = models.AutoField(primary_key = True)
    roleDelete = models.BooleanField(default=False)
    roleName = models.TextField()
    roleDescription = models.TextField()
    roleCreated = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.roleName
    
class Permission(models.Model): 
    permissionID = models.AutoField(primary_key = True)
    permissionAuthorization = models.ForeignKey(Authorization)
    permissionRole = models.ForeignKey(Role)
    permissionActive = models.BooleanField(default=False)
    permissionCreated = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        if self.permissionActive:
            return 'have'
        else:
            return "haven't"
class Account(models.Model):
    accountID = models.AutoField(primary_key = True)
    accountUser = models.ForeignKey(User)
    accountAuthorization = models.ForeignKey(Authorization)
    accountAvatar = models.ForeignKey(File, null = True)
    accountGender = models.BooleanField(default=False) 
    accountBirthday = models.DateField()
    accountAddress = models.TextField(blank=True)
    accountActive = models.BooleanField(default=False)
    accountCreated = models.DateTimeField(auto_now_add=True)
    ProficiencyTest = models.BooleanField(default=False)
    ProficiencyTestScores = models.FloatField(null = True)
    def __unicode__(self):
#         user = Use
        return self.accountUser.username

def FullAccount(User):
        account = Account.objects.get(accountUser = User)
        return dict( 
                    accountID = account.accountID,
                    accountUser = account.accountUser.id,
                    last_name = account.accountUser.last_name,
                    first_name = account.accountUser.first_name,
                    last_login = str(account.accountUser.last_login),
                    date_joineds = str(account.accountUser.date_joined),
                    accountGender = account.accountGender,
                    accountAvatar = account.accountAvatar.fileName,
                    accountAddress = account.accountAddress,
                    accountBirthday = str(account.accountBirthday),
                    )
        
def SimpleAccount(User):
    account = Account.objects.get(accountUser = User)
    return dict( 
                accountID = account.accountID,
                accountUser = account.accountUser.id,
                last_name = account.accountUser.last_name,
                first_name = account.accountUser.first_name,
                accountAvatar = account.accountAvatar.fileName,
                    )
    
class Level(models.Model):
    levelID = models.AutoField(primary_key = True)
    levelAuthor = models.ForeignKey(User)
    levelName = models.TextField()
    levelDescription = models.TextField()
    levelCreated = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.levelName
    def as_json(self):
        return dict(levelID = str(self.levelID),
                    levelName = str(self.levelName),
                    levelDescription = str(self.levelDescription),
                    )


class Option(models.Model):
    optionID = models.AutoField(primary_key = True)
    optionName = models.TextField()
    optionKey = models.SlugField()
    optionDescription = models.TextField()
    optionDelete = models.BooleanField(default=False)
    optionCreated = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.optionName
class Type(models.Model):
    typeID = models.AutoField(primary_key = True)
    TypeOption = models.ForeignKey(Option)
    typeName = models.TextField()
    typeKey = models.SlugField()
    typeDescription = models.TextField()
    typeDelete = models.BooleanField(default=False)
    typeCreated = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.typeName
    def as_json(self):
        return dict(typeID = self.typeID,
                    typeName = self.typeName,
                    typeKey = self.typeKey,
                    TypeOption = self.TypeOption.optionKey,
                    typeDescription = self.typeDescription,
                    )

class University(models.Model):
    universityID = models.AutoField(primary_key = True)
    universityName = models.TextField()
    universityType = models.ForeignKey(Type)
    universityLogo = models.ForeignKey(File, null = True)
    universityInfor =  models.TextField()
    universityAuthor = models.ForeignKey(User)
    universityDelete = models.BooleanField(default=False)
    universityCreated = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.universityName
    def as_json(self):
        return dict(universityID = self.universityID,
                    universityLogo = self.universityLogo.fileName,
                    universityName = self.universityName,
                    universityInfor = self.universityInfor,
                    )
    
class Course(models.Model):
    courseID = models.AutoField(primary_key = True)
    courseAuthor = models.ForeignKey(User)
    courseLevel = models.ForeignKey(Level)
    courseName = models.TextField()
    courseDescription = models.TextField()
    courseDelete = models.BooleanField(default=False)
    courseCreated = models.DateTimeField(auto_now_add=True)
    courseUniversity = models.ForeignKey(University,blank=True)
    def __unicode__(self):
        return self.courseName
    def as_json(self):
        return dict(
                    courseID = str(self.courseID),
                    courseAuthor = str(self.courseAuthor.id),
                    courseLevel = str(json.dumps(self.courseLevel.as_json())),
                    courseName = str(self.courseName),
                    courseDescription = str(self.courseDescription),
                    )
class Unit(models.Model):
    unitID = models.AutoField(primary_key = True)
    unitAuthor = models.ForeignKey(User)
    unitCourse = models.ForeignKey(Course)
    unitType = models.ForeignKey(Type)
    unitName = models.TextField()
    unitDescription = models.TextField()
    unitDelete = models.BooleanField(default=False)
    unitCreated = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.unitName
    def as_json(self):
        return dict(unitID = self.unitID,
                    unitName = self.unitName,
                    unitDescription = self.unitDescription,
                    unitCourse = self.unitCourse.courseName,
                    )
class Question(models.Model):
    questionID = models.AutoField(primary_key = True)
    questionUnit = models.ForeignKey(Unit)
    questionAuthor = models.ForeignKey(User)
    questionType = models.ForeignKey(Type, related_name='Type')
    questionSkill = models.ForeignKey(Type, related_name='Skill')
    questionTitle = models.TextField()
    questionContents = models.TextField()
#     questionType = models.IntegerField()
    questionDelete = models.BooleanField(default=False)
    questionCreated = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.questionTitle
    def as_json(self):
        return dict(questionID = str(self.questionID),
                    questionUnit = str(json.dumps(self.questionUnit.as_json())),
                    questionAuthor = str(json.dumps(UserDict(self.questionAuthor))),
                    questionType = str(json.dumps(self.questionType.as_json())),
                    questionSkill = str(json.dumps(self.questionSkill.as_json())),
                    questionTitle = self.questionTitle,
                    questionContents = self.questionContents,
                    questionCreated = str(self.questionCreated),
                    )
class Answer(models.Model):
    answerID = models.AutoField(primary_key = True)
    answerUser = models.ForeignKey(User)
    answerQuestion = models.ForeignKey(Question)
    answerContent = models.TextField()
    answerScore = models.FloatField()
    answerReason = models.TextField(blank=True)    
    answerCreated = models.DateTimeField(auto_now_add=True)
    answerDelete = models.BooleanField(default=False)
    def as_json(self):
        return dict(
                    answerUser = str(json.dumps(UserDict(self.answerUser))),
                    answerID = self.answerID,
                    answerQuestion = str(json.dumps(self.answerQuestion.as_json())),
                    answerContent = self.answerContent,
                    answerScore = self.answerScore,
                    answerReason = self.answerReason,
                    answerCreated = str(self.answerCreated),
                    )
    
    
class Classroom(models.Model):
    classroomID = models.AutoField(primary_key = True)
    classroomUser = models.ForeignKey(User,blank =True)
    classroomCourse = models.ForeignKey(Course)
    classroomRole = models.ForeignKey(Type)
    classroomCode = models.TextField(blank = True)
    classroomActive = models.BooleanField(default=False)
    classroomCreated = models.DateTimeField(auto_now_add=True)    
    def as_json(self):
        return dict(
                    classroomID = self.classroomID,
                    classroomUser= str(json.dumps(UserDict(self.classroomUser))),
                    classroomCourse = str(json.dumps(self.classroomCourse.as_json())),
                    classroomRole = str(json.dumps(self.classroomRole.as_json())),
                    classroomCreated = str(self.classroomCreated)
                    )
class Discussion(models.Model):
    discussionID = models.AutoField(primary_key = True)
    discussionCourse = models.ForeignKey(Course)
    discussionName = models.TextField()
    discussionDescription = models.TextField(blank = True)
    discussionCreated = models.DateTimeField(auto_now_add=True)
    discussionDelete = models.BooleanField(default=False)
    def __unicode__(self):
        return self.discussionName
    
class Group(models.Model):
    groupID = models.AutoField(primary_key = True)
    groupName = models.TextField()
    groupUser = models.ForeignKey(User)
    groupDiscussion = models.ForeignKey(Discussion)
    groupRole = models.ForeignKey(Type)
    groupActive = models.BooleanField(default=False)
    groupCreated = models.DateTimeField(auto_now_add=True)  
    
class Status(models.Model):
    statusID = models.AutoField(primary_key = True)
    statusAuthor = models.ForeignKey(User)
    statusDiscussion = models.ForeignKey(Discussion)
    statusContent = models.TextField()
    statusDelete = models.BooleanField(default=False)
    statusCreated = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-statusCreated']
    def __unicode__(self):
        return self.statusContent
    def as_json(self):
        return dict(
                    statusID = self.statusID,
                    statusAuthorid = self.statusAuthor.id,
                    statusAuthor = str(json.dumps(SimpleAccount(self.statusAuthor))) ,
                    statusDiscussion = self.statusDiscussion.discussionCourse.courseName,
                    statusContent = self.statusContent,
                    statusCreated = str(self.statusCreated),
                    )
class CommentStatus(models.Model):
    commentID = models.AutoField(primary_key = True)
    commentAuthor = models.ForeignKey(User)
    commentStatus = models.ForeignKey(Status)
    commentContent = models.TextField()
    commentDelete = models.BooleanField(default=False)
    commentCreated = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.commentContent
    def as_json(self):
        return dict(
                    commentID = self.commentID,
                    commentAuthorID = self.commentAuthor.id,
                    commentAuthor = str(json.dumps(SimpleAccount(self.commentAuthor))),
                    commentContent = self.commentContent,
                    commentCreated = str(self.commentCreated),
                    )
    
class LikeStatus(models.Model):
    likeID = models.AutoField(primary_key = True)
    likeAuthor = models.ForeignKey(User)
    likeStatus = models.ForeignKey(Status)
    likeContent = models.BooleanField(default=False)
    likeCreated = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return str(self.likeContent)
    def as_json(self):
        return dict(
                    likeID = self.likeID,
                    likeAuthorID = self.likeAuthor.id,
                    likeAuthor = self.likeAuthor.last_name +' '+ self.likeAuthor.first_name,
                    )
class BonusStatus(models.Model):
    bonusID = models.AutoField(primary_key = True)
    bonusAuthor = models.ForeignKey(User)
    bonusStatus = models.ForeignKey(Status)
    bonusContent = models.BooleanField(default=False)
    bonusCreated = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.bonusContent


class LikeComment(models.Model):
    likeID = models.AutoField(primary_key = True)
    likeAuthor = models.ForeignKey(User)
    likeComment = models.ForeignKey(CommentStatus)
    likeContent = models.BooleanField(default=False)
    likeCreated = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return str(self.likeContent)
    def as_json(self):
        return dict(
                    likeID = self.likeID,
                    likeAuthorID = self.likeAuthor.id,
                    likeAuthor = self.likeAuthor.last_name +' '+ self.likeAuthor.first_name,
                    )
class BonusComment(models.Model):
    bonusID = models.AutoField(primary_key = True)
    bonusAuthor = models.ForeignKey(User)
    bonusComment = models.ForeignKey(CommentStatus)
    bonusContent = models.BooleanField(default=False)
    bonusCreated = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.bonusContent
    
    
class Archive(models.Model):
    archiveID = models.AutoField(primary_key = True)
    archiveAuthor = models.ForeignKey(User)
    archiveCourse = models.ForeignKey(Course)
    archiveFile = models.ForeignKey(File)
    archiveName = models.TextField()  
    archiveDescription = models.TextField()    
    archiveDelete = models.BooleanField(default=False)
    archiveCreated = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.archiveName

