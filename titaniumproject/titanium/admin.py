from django.contrib import admin
from titanium.models import *

class SystemErrorLogAdmin(admin.ModelAdmin):
    ordering = ('-timestamp',)
    list_display = ('level', 'message', 'timestamp',)
    list_filter = ('level',)
    search_fields = ('level','message',)

    def has_add_permission(self, request):
        return False

    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields + ('level', 'message', 'timestamp')
admin.site.register(SystemErrorLog, SystemErrorLogAdmin)

class OptionAdmin(admin.ModelAdmin):
    ordering = ('-optionCreated',)
    list_display = ('optionID', 'optionName', 'optionKey','optionDescription','optionDelete','optionCreated')
    list_filter = ('optionDelete',)
    search_fields = ('optionID','optionName',)
admin.site.register(Option,OptionAdmin)

class TypeAdmin(admin.ModelAdmin):
    ordering = ('-typeCreated',)
    list_display = ('typeID', 'TypeOption', 'typeName','typeKey','typeDescription','typeDelete','typeCreated')
    list_filter = ('TypeOption',)
    search_fields = ('typeID','typeName',)
admin.site.register(Type,TypeAdmin)

class FileAdmin(admin.ModelAdmin):
    ordering = ('-fileCreated',)
    list_display = ('fileID', 'fileFile', 'fileName','fileCategory','fileUser','fileDelete','fileCreated')
    list_filter = ('fileCategory',)
    search_fields = ('fileID','fileName',)
admin.site.register(File,FileAdmin)

class AuthorizationAdmin(admin.ModelAdmin):
    ordering = ('-authorizationCreated',)
    list_display = ('authorizationID', 'authorizationName', 'authorizationDescription','authorizationDelete','authorizationCreated')
    list_filter = ('authorizationDelete',)
    search_fields = ('authorizationID','authorizationName',)
admin.site.register(Authorization,AuthorizationAdmin)

class RoleAdmin(admin.ModelAdmin):
    ordering = ('-roleCreated',)
    list_display = ('roleID', 'roleName', 'roleDescription','roleDelete','roleCreated')
    list_filter = ('roleDelete',)
    search_fields = ('roleID','roleName',)
admin.site.register(Role,RoleAdmin)

class PermissionAdmin(admin.ModelAdmin):
    ordering = ('-permissionCreated',)
    list_display = ('permissionID', 'permissionAuthorization', 'permissionRole','permissionActive','permissionCreated')
    list_filter = ('permissionActive','permissionRole',)
    search_fields = ('permissionID','permissionAuthorization',)
admin.site.register(Permission,PermissionAdmin)

class AccountAdmin(admin.ModelAdmin):
    ordering = ('-accountCreated',)
    list_display = ('accountID', 'accountUser', 'accountAuthorization','accountAvatar','accountGender','accountBirthday','accountAddress','accountActive','accountCreated','ProficiencyTest','ProficiencyTestScores')
    list_filter = ('accountActive','accountAuthorization',)
    search_fields = ('accountID','accountUser',)
admin.site.register(Account,AccountAdmin)

class AnswerAdmin(admin.ModelAdmin):
    ordering = ('-answerCreated',)
    list_display = ('answerID', 'answerUser', 'answerQuestion','answerScore','answerReason','answerCreated')
    list_filter = ('answerUser',)
    search_fields = ('answerUser','answerQuestion',)
admin.site.register(Answer,AnswerAdmin)

class LevelAdmin(admin.ModelAdmin):
    ordering = ('-levelCreated',)
    list_display = ('levelID', 'levelAuthor', 'levelName','levelDescription','levelCreated')
    list_filter = ('levelAuthor',)
    search_fields = ('levelName',)
admin.site.register(Level,LevelAdmin)

class UniversityAdmin(admin.ModelAdmin):
    ordering = ('-universityCreated',)
    list_display = ('universityID', 'universityName', 'universityInfor','universityType','universityAuthor','universityDelete','universityCreated','universityLogo')
    list_filter = ('universityType',)
    search_fields = ('universityName',)
admin.site.register(University,UniversityAdmin)

class CourseAdmin(admin.ModelAdmin):
    ordering = ('-courseUniversity',)
    list_display = ('courseID', 'courseAuthor','courseUniversity', 'courseLevel','courseName','courseDescription','courseDelete','courseCreated')
    list_filter = ('courseUniversity',)
    search_fields = ('courseName',)
admin.site.register(Course,CourseAdmin)

class UnitAdmin(admin.ModelAdmin):
    ordering = ('-unitCreated',)
    list_display = ('unitID', 'unitAuthor','unitCourse', 'unitType','unitName','unitDescription','unitDelete','unitCreated')
    list_filter = ('unitCourse',)
    search_fields = ('unitName',)
admin.site.register(Unit,UnitAdmin)

class QuestionAdmin(admin.ModelAdmin):
    ordering = ('-questionCreated',)
    list_display = ('questionID', 'questionUnit','questionAuthor', 'questionType','questionTitle','questionContents','questionDelete','questionCreated')
    list_filter = ('questionType','questionAuthor')
    search_fields = ('questionID','questionContents','questionUnit')
admin.site.register(Question,QuestionAdmin)

class ClassroomAdmin(admin.ModelAdmin):
    ordering = ('-classroomCreated',)
    list_display = ('classroomID', 'classroomUser','classroomCourse', 'classroomCode','classroomActive','classroomCreated')
    list_filter = ('classroomCourse',)
    search_fields = ('classroomID','classroomCode','classroomUser')
admin.site.register(Classroom,ClassroomAdmin)

class DiscussionAdmin(admin.ModelAdmin):
    ordering = ('-discussionCreated',)
    list_display = ('discussionID', 'discussionCourse','discussionName', 'discussionDescription','discussionCreated','discussionDelete')
    list_filter = ('discussionCourse',)
    search_fields = ('discussionID','discussionName','discussionDescription')
admin.site.register(Discussion,DiscussionAdmin)

class GroupAdmin(admin.ModelAdmin):
    ordering = ('-groupCreated',)
    list_display = ('groupID', 'groupName','groupUser', 'groupDiscussion','groupRole','groupActive','groupCreated')
    list_filter = ('groupDiscussion',)
    search_fields = ('groupName','groupUser','groupDiscussion')
admin.site.register(Group,GroupAdmin)

class StatusAdmin(admin.ModelAdmin):
    ordering = ('-statusCreated',)
    list_display = ('statusID', 'statusAuthor','statusDiscussion', 'statusContent','statusDelete','statusCreated')
    list_filter = ('statusDiscussion',)
    search_fields = ('statusID','statusAuthor','statusContent')
admin.site.register(Status,StatusAdmin)

class CommentStatusAdmin(admin.ModelAdmin):
    ordering = ('-commentCreated',)
    list_display = ('commentID', 'commentAuthor','commentStatus', 'commentContent','commentDelete','commentCreated')
    list_filter = ('commentStatus',)
    search_fields = ('commentID','commentContent')
admin.site.register(CommentStatus,CommentStatusAdmin)

class LikeStatusAdmin(admin.ModelAdmin):
    ordering = ('-likeCreated',)
    list_display = ('likeID', 'likeAuthor','likeStatus', 'likeContent','likeCreated')
    list_filter = ('likeStatus',)
    search_fields = ('likeID','likeAuthor','likeStatus')
admin.site.register(LikeStatus,LikeStatusAdmin)

class BonusStatusAdmin(admin.ModelAdmin):
    ordering = ('-bonusCreated',)
    list_display = ('bonusID', 'bonusAuthor','bonusStatus', 'bonusContent','bonusCreated')
    list_filter = ('bonusStatus',)
    search_fields = ('bonusID','bonusAuthor','bonusStatus')
admin.site.register(BonusStatus,BonusStatusAdmin)

class LikeCommentAdmin(admin.ModelAdmin):
    ordering = ('-likeCreated',)
    list_display = ('likeID', 'likeAuthor','likeComment', 'likeContent','likeCreated')
    list_filter = ('likeComment',)
    search_fields = ('likeID','likeAuthor','likeComment')
admin.site.register(LikeComment,LikeCommentAdmin)

class BonusCommentAdmin(admin.ModelAdmin):
    ordering = ('-bonusCreated',)
    list_display = ('bonusID', 'bonusAuthor','bonusComment', 'bonusContent','bonusCreated')
    list_filter = ('bonusComment',)
    search_fields = ('bonusID','bonusAuthor','bonusComment')
admin.site.register(BonusComment,BonusCommentAdmin)

class ArchiveAdmin(admin.ModelAdmin):
    ordering = ('-archiveCreated',)
    list_display = ('archiveID', 'archiveAuthor','archiveCourse', 'archiveFile','archiveName','archiveDescription', 'archiveDelete','archiveCreated')
    list_filter = ('archiveCourse',)
    search_fields = ('archiveID','archiveCourse','archiveName')
admin.site.register(Archive,ArchiveAdmin)