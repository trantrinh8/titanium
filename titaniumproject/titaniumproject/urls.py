from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from titanium.controllers import*
from titanium.views import*
from archive.views import*
from archive.distributor import *
from discussion.views import*
from discussion.distributor import*
from activity.views import*
from activity.distributor import*
from titanium.distributor import*


urlpatterns = patterns('',
    # Examples:
#     url(r'^$', 'titaniumproject.views.index', name='index'),
#     url(r'^index/$', 'titaniumproject.views.base', name='base'),
#     url(r'^course/$', 'titaniumproject.views.course', name='course'),
    # url(r'^titaniumproject/', include('titaniumproject.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
#     url(r'^', include('titanium.urls', namespace = "titanium")),
# titanium - controllers
    url(r'^login', LoginView, name='login'),
    url(r'^logout', LogoutView, name='logout'),
# titanium - views
    url(r'^index', Index, name='index'),
    url(r'^myprofile', MyProfile, name='myprofile'),
    url(r'^$', Base, name='base'),
    url(r'^course', CourseView, name='course'),
    url(r'^signup',Signup,name='signup'),
    url(r'^helps',helps,name='helps'),
    url(r'^registerschool',registerschool,name='registerschool'),
# titanium - distributor
    url(r'^testemail', TestEmail, name='testemail'),
    url(r'^getuser', GetUser, name='getuser'),
    url(r'^getcourse', GetCourse, name='getcourse'),
    url(r'^getquestionunit', GetQuestionUnit, name='getquestionunit'),
    url(r'^getquestion', GetQuestion, name='getquestion'),
    url(r'^setquestion', SetQuestion, name='setquestion'),
    url(r'^setunit', SetUnit, name='setunit'),
    url(r'^getmyclass', GetMyClass, name='getmyclass'),
    url(r'^setcourse',SetCourse,name='setcourse'),
    url(r'^setanswer',setAnswer,name='setanswer'),
    url(r'^getfulluser',getFullUser,name='getfulluser'),
    url(r'^getalluniversity',getAlluniversity,name='getalluniversity'),
# Activity - views
    url(r'^activity', ActivityViews, name='activity'),
# Activity - distributor
    url(r'^getmyactivity', Getmyactivity, name='getmyactivity'),
# Discussion - views
    url(r'^discussion', DiscussionViews, name='discussion'),
    url(r'^setstatus', Setstatus, name='setstatus'),
    url(r'^getstatus', Getstatus, name='getstatus'),
    url(r'^setcomment', Setcomment, name='setcomment'),
    url(r'^setlike',Setlike,name = 'setlike'),
    url(r'^removelike',Removelike,name = 'removelike'),
    
# Discussion - distributor

# Archive - views
    url(r'^archive',ArchiveViews,name='archive'),
    url(r'^getmyfile',Getmyfile,name='getmyfile'),
# Archive - distributor
    url(r'^uploadfile',Uploadfile,name='uploadfile'),
    url(r'^setavatar',Setavatar,name='setavatar'),
    
# error 404
    url(r'^(?P<error>\w+)',error404, name="error404"),
)
