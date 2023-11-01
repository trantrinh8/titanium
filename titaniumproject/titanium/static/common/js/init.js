'use strict';
var app=angular.module("titanium",['ngSanitize','ngCookies','ngRoute','ngDragDrop','angularFileUpload']).config(function($routeProvider,$httpProvider) {
	// var titanium=$('body').attr('titanium');
	// var redirect='login';
	// if (!isEmpty(titanium)) {
		// redirect="/course";
	// };
	// console.log(redirect);
	$routeProvider.when('/index', {
		templateUrl: '/index',
		controller: indexController
	}).when('/course', {
		templateUrl: '/course',
		controller: courseController
	 }).when('/activity', {
		 templateUrl: '/activity',
		 controller: activityController
	 }).when('/archive', {
		 templateUrl: 'archive',
		 controller: archiveController
	 }).when('/discussion', {
		 templateUrl: '/discussion',
		 controller: discussionController
	}).when('/myprofile', {
		 templateUrl: '/myprofile',
		 controller: myprofileController
	}).when('/registerschool', {
		 templateUrl: '/registerschool',
		 controller: registerschoolController
	}).	otherwise({
		redirectTo: '/course'
	});
  $httpProvider.defaults.headers.put['Content-Type'] ='application/x-www-form-urlencoded; charset=UTF-8';
  $httpProvider.defaults.headers.post['Content-Type'] ='application/x-www-form-urlencoded; charset=UTF-8';
  
  // $httpProvider.defaults.headers.post["X-CSRFToken"] = 'http://schemas.microsoft.com/sharepoint/soap/UpdateListItems';
}).directive('ngThumb', ['$window', function($window) {
        var helper = {
            support: !!($window.FileReader && $window.CanvasRenderingContext2D),
            isFile: function(item) {
                return angular.isObject(item) && item instanceof $window.File;
            },
            isImage: function(file) {
                var type =  '|' + file.type.slice(file.type.lastIndexOf('/') + 1) + '|';
                return '|jpg|png|jpeg|bmp|gif|'.indexOf(type) !== -1;
            }
        };

        return {
            restrict: 'A',
            template: '<canvas/>',
            link: function(scope, element, attributes) {
                if (!helper.support) return;

                var params = scope.$eval(attributes.ngThumb);

                if (!helper.isFile(params.file)) return;
                if (!helper.isImage(params.file)) return;

                var canvas = element.find('canvas');
                var reader = new FileReader();

                reader.onload = onLoadFile;
                reader.readAsDataURL(params.file);

                function onLoadFile(event) {
                    var img = new Image();
                    img.onload = onLoadImage;
                    img.src = event.target.result;
                }

                function onLoadImage() {
                    var width = params.width || this.width / this.height * params.height;
                    var height = params.height || this.height / this.width * params.width;
                    canvas.attr({ width: width, height: height });
                    canvas[0].getContext('2d').drawImage(this, 0, 0, width, height);
                }
            }
        };
    }]);
    

function indexController() {
  
};
function baseController($scope,$http,$location,$filter,$cookies) {
	$scope.course={};
	$scope.unitOption=[];
	$scope.questionOption=[];
	$scope.skillOption=[];
	
	$scope.allCourse=[];
	$http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
	var xsrf = $.param({
						usr:$('body').attr('titanium'),
						authorization: $('body[authorization]').attr('authorization')
						});
	$http({method: 'POST',url: '/getuser',data: xsrf,}).success(function(data, status) {
		$scope.user = data;	
		console.log($scope.user);
	});
	$scope.email_Ok = 0;
	$scope.pass_Ok = 0;
	$scope.sigup_ok = 0;
	$scope.create_user = function(){
		$scope.message_signup ='';
		if($scope.email){
			
		$http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
		var xsrf = $.param({
							email:$scope.email,
							usr:$('body').attr('titanium'),
							authorization: $('body[authorization]').attr('authorization')
							});
		$http({method: 'POST',url: '/testemail',data: xsrf,}).success(function(data, status) {
			
			if(!data.message){
				$scope.message_signup = $scope.message_signup + "Email name already exists, please try with another email!";
				$scope.email_Ok = 2;
				$scope.sigup_ok = 0;
			}else{
				$scope.email_Ok = 1;
			}
		});
	}
	if($scope.password != $scope.confirmpassword)
	{
		$scope.sigup_ok = 0;
		$scope.pass_Ok = 1;
		$scope.message_signup = $scope.message_signup + "confirm email don't correct!";
	}else{
		$scope.pass_Ok = 0;
	}
	if($scope.pass_Ok == 0 && $scope.email_Ok ==1){
		
		$http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
		var xsrf = $.param({
							email:$scope.email,
							password:$scope.password,
							firstname:$scope.firstname,
							lastname:$scope.lastname,
							gender: $scope.gender,
							birthday: new Date($scope.birthday).toISOString(),
							usr:$('body').attr('titanium'),
							authorization: $('body[authorization]').attr('authorization')
							});
		$http({method: 'POST',url: '/signup',data: xsrf,}).success(function(data, status) {
				$scope.sigup_ok = 1;
		});
	}
	console.log($scope.birthday);
	};
	
};
	
function courseController($scope,$http,$location,$filter,$cookies) {
	$scope.start = 1;
	$scope.showyourclass = function(){
		//get my class
	$http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
	var xsrf = $.param({
						usr:$('body').attr('titanium'),
						authorization: $('body[authorization]').attr('authorization')
						});
	$http({method: 'POST',url: '/getmyclass',data: xsrf,}).success(function(data, status) {
		
		$scope.myclass = data;
		for(var i=0; i<data.myclass.length;i++)
		{
			var a = $scope.myclass.myclass[i].classes;
			$scope.myclass.myclass[i].classes = JSON.parse(a);
			var b = $scope.myclass.myclass[i].classes.classes.classroomCourse;
			$scope.myclass.myclass[i].classes.classes.classroomCourse = JSON.parse(b);
			b = $scope.myclass.myclass[i].classes.classes.classroomCourse.courseLevel;
			$scope.myclass.myclass[i].classes.classes.classroomCourse.courseLevel = JSON.parse(b);
			b = $scope.myclass.myclass[i].classes.classes.classroomRole;
			$scope.myclass.myclass[i].classes.classes.classroomRole = JSON.parse(b);
			b = $scope.myclass.myclass[i].classes.classes.classroomUser;
			$scope.myclass.myclass[i].classes.classes.classroomUser = JSON.parse(b);
			for(var j=0; j<$scope.myclass.myclass[i].classes.unit.length;j++)
			{
				b = $scope.myclass.myclass[i].classes.unit[j].unit;
				$scope.myclass.myclass[i].classes.unit[j].unit = JSON.parse(b);
				for (var k=0;k<$scope.myclass.myclass[i].classes.unit[j].unit.question.length;k++)
				{
					b = $scope.myclass.myclass[i].classes.unit[j].unit.question[k].questionContents;
					$scope.myclass.myclass[i].classes.unit[j].unit.question[k].questionContents = JSON.parse(b);
					b = $scope.myclass.myclass[i].classes.unit[j].unit.question[k].questionAuthor;
					$scope.myclass.myclass[i].classes.unit[j].unit.question[k].questionAuthor = JSON.parse(b);
					b = $scope.myclass.myclass[i].classes.unit[j].unit.question[k].questionSkill;
					$scope.myclass.myclass[i].classes.unit[j].unit.question[k].questionSkill = JSON.parse(b);
					b = $scope.myclass.myclass[i].classes.unit[j].unit.question[k].questionType;
					$scope.myclass.myclass[i].classes.unit[j].unit.question[k].questionType = JSON.parse(b);
					b = $scope.myclass.myclass[i].classes.unit[j].unit.question[k].questionUnit;
					$scope.myclass.myclass[i].classes.unit[j].unit.question[k].questionUnit = JSON.parse(b);
				}
			}
		}
		console.log($scope.myclass);
	});
	// show my class
		$scope.start = 0;
	};
	$scope.allcourse =function(){
		$('#all_course').modal('show');
	};
	
	
	// get all course
	$scope.showCourse = 'allCourse';
	$http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
	var xsrf = $.param({
						usr:$('body').attr('titanium'),
						authorization: $('body[authorization]').attr('authorization')
						});
	$http({method: 'POST',url: '/getcourse',data: xsrf,}).success(function(data, status) {
		for(var i = 0; i < data.allSkill.length; i++){
			if(data.allSkill[i].TypeOption == 'unit'){
				$scope.unitOption.push(data.allSkill[i]);
			}
			else if(data.allSkill[i].TypeOption == 'question'){
				$scope.questionOption.push(data.allSkill[i]);
			}
			else if(data.allSkill[i].TypeOption == 'skill'){
				$scope.skillOption.push(data.allSkill[i]);
			}
		}
		$scope.allCourse = data.allCourse;
		
		console.log(data);
		$scope.course=data;
		for(var i =0; i <data.allCourse.length;i++)
		{
			var a = $scope.course.allCourse[i].courseLevel;
			$scope.course.allCourse[i].courseLevel = JSON.parse(a);
		}
    }).error(function(data, status) {
  	});
  	
	///////////////////////set class////////////////////
	$scope.newclass = function(){
		$('#class-modal').modal('show');
	};
	$scope.savecourse = function(){
			$http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
			var xsrf = $.param({
									levelcourse:$scope.levelCourse.levelName,
									courseName:$scope.courseName,
									courseDescription:$scope.courseDescription				
					});
		  	$http({method:'POST',url: '/setcourse',data: xsrf,}).success(function(data){
				console.log(data);
				$scope.allCourse.push(data.course);
				$('#class-modal').modal('hide');
				$scope.levelCourse={};
				$scope.courseName ='';
				$scope.courseDescription ='';
			});
	};
	
	////////          set Question./////////////////////
	$scope.aut = $('body[authorization]').attr('authorization');
	$scope.unitModalTitle="";
	$scope.questions ={};
	$scope.questions.listAnswer = [{
  			'key' : 'A',
  			'value' : '',
  			'helptext' : '',
  		},{
  			'key' : 'B',
  			'value' : '',
  			'helptext' : '',
  		}
  		];
  		$scope.questions.answer = [];
  		$scope.choice = ['column label','row label'];
  		$scope.choice1 = ['column label','row label','words to choose'];
  		$scope.choice2 = ['column label','words to choose'];
  		$scope.choice3 = ['row label','words to choose'];
  		$scope.choicefw =['words to choose','form fill'];
  		//show tất cả các khóa học từ level
		$scope.showlevel =function(level){
			$('#showlevel').modal('show');
			$scope.levelcopy = level;
		};
		//kết thúc
		//show tất cả các khóa học từ level
		$scope.showcourse =function(clas){
			$('#showlevel').modal('hide');
			$('#showcourse').modal('show');
			$scope.coursecopy = clas;
		};
		//kết thúc
		//show tất cả các câu hỏi từ skill
		$scope.showskill =function(skill){
			
			$('#showskill').modal('show');
			$scope.coursecopy = skill;
		};
		//kết thúc
	$scope.pagination=0;
  	$scope.paginationChoice = function(choice){
  		
  		console.log($scope.questions.listAnswer.length);
  		console.log(choice.key);
  		if(choice == 'next'){
  			if($scope.pagination == $scope.questions.listAnswer.length -1 ){
  				$scope.pagination = 0;
  			}else{
  				$scope.pagination += 1;
  			}
  		}else if(choice == 'prew'){
  			if($scope.pagination == 0){
  				$scope.pagination = $scope.questions.listAnswer.length -1;
  			}else{
  				$scope.pagination -= 1;
  			}
  		}else{
  			$scope.pagination = choice;
  		}
  		console.log($scope.pagination);
  	};
  $scope.newUnit = function () {
    $('#unit-modal').modal('show');
    $scope.unitModalTitle="New Unit";
  };
  //thêm câu hỏi
  $scope.newQuestion = function(){
  	$('#question-modal').modal('show');
    $scope.unitModalTitle="New Question";
  };
  	//đẩy dữ liệu question.
  //	$http({method: 'GET', url: '/nearbySearchSave',async:false,params:para}).success(function(data, status, headers, config) {	
//						console.log(data)
	//				})
  	
  	$scope.savequestion = function(){
  	$http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
  	console.log($scope.questions);
  	
	var xsrf = $.param({unit:$scope.questions.questionUnit.unitName
		,skill:$scope.questions.questionSkill.typeName
		,type:$scope.questions.questionType.typeName
		,title:$scope.questions.questionTitle
		,questionContents : JSON.stringify({
			'contents':$scope.questions.contents,
			'listAnswer':$scope.questions.listAnswer,
			'answer':$scope.questions.answer,
		})	
		});
	$http({method:'POST',url: '/setquestion',data: xsrf,}).success(function(data){
		$scope.questionr = data.question;
		console.log('getquestion');
		console.log(data);
		$('#question-modal').modal('hide');
		$scope.questions ={};
		$scope.questions.listAnswer = [{
  			'key' : 'A',
  			'value' : '',
  			'helptext' : '',
  			'keyinput':'',
  		},{
  			'key' : 'B',
  			'value' : '',
  			'helptext' : '',
  			'keyinput':'',
  		}
  		];
  		$scope.questions.answer = [];
	});
  	};
  	
  	
  	$scope.saveunit = function(){
  		$http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
	var xsrf = $.param({unitcourse:$scope.unitCourse.courseName
		,unittype:$scope.unitType.typeName
		,name:$scope.unitName
		,description:$scope.unitDescription	
		});
	$http({method:'POST',url: '/setunit',data: xsrf,}).success(function(data){
		$scope.course.allUnit.push(data.unit);
		console.log('getquestion');
		console.log(data);
		$('#unit-modal').modal('hide');
		$scope.unitCourse= {};
		$scope.unitType ={};
		$scope.unitName ='';
		$scope.unitDescription ='';
	});
  	};
  	$scope.addChoiceAnswer = function(){
  		$scope.questions.listAnswer.push({
  			'key' : String.fromCharCode(65 + $scope.questions.listAnswer.length),
  			'value' : '',
  			'helptext' : '',
  			'keyinput':'',
  		});
  	};
  	var as={};
  	$scope.removeLastChoiceAnswer = function(){
  		if($scope.questions.listAnswer.length > 1){
  			$scope.questions.listAnswer.pop();
  			
  		}
  		
  	};
  	
  	$scope.removeAnswer = function(){
		$scope.questions.answer = [];
	  };
  	$scope.addAnswer = function(){
  		$scope.questions.answer.push($scope.as);
  	};
  	$scope.addcrAnswer= function(){
  		as = {'column':$scope.ascl,
  		 'row':$scope.asr};
  		$scope.questions.answer.push(as);
  	};
  	$scope.addcrddAnswer = function(){
  		as = {
  			'column':$scope.ascl,
  		 'row':$scope.asr,
  		 'choose':$scope.asch
  		};
  		$scope.questions.answer.push(as);
  	};
  	$scope.addcddAnswer = function(){
  		as = {
  			'column':$scope.ascl,
  		 'choose':$scope.asch
  		};
  		$scope.questions.answer.push(as);
  	};
  	$scope.addrddAnswer = function(){
  		as = {
  			'row':$scope.asr,
  		 'choose':$scope.asch
  		};
  		$scope.questions.answer.push(as);
  	};
	$scope.addinddAnswer = function(){
  		as = {
  			'key':$scope.askey,
  		 'answer':$scope.ascl
  		};
  		$scope.questions.answer.push(as);
  	};
  	$scope.starts = function(){
  		$( "#rocket" ).animate({
  			top: "-=1000px",
		    left: "+=1500px",
		  }, 1500, function() {
		    $scope.qs_index = 0;
		    $( "#rocket" ).hide();
		  });
		
  	};
  	$scope.Loadquestion = function(unit){
  		$('.loadweb').show();
  		$('#showcourse').modal('hide');
  		$('#questions-modal').modal('show');
  		$scope.qs_index = -1;
  		$( "#rocket" ).show();
  		$( "#rocket" ).animate({
  			top: "200px",
		    left: "0px",
		  }, 1500);
		$scope.modal_title = unit.unitName;
  		$http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
		var xsrf = $.param({unitid:unit.unitID});
		$http({method:'POST',url: '/getquestionunit',data: xsrf,}).success(function(data){
			$scope.question_unit = data.questions ;
			for(var i = 0; i < data.questions.length; i++)
			{
				var s = $scope.question_unit[i].questionContents;
				$scope.question_unit[i].questionContents = JSON.parse(s);
				var a = $scope.question_unit[i].questionAuthor;
				$scope.question_unit[i].questionAuthor = JSON.parse(a);
				var b = $scope.question_unit[i].questionSkill;
				$scope.question_unit[i].questionSkill = JSON.parse(b);
				var c = $scope.question_unit[i].questionType;
				$scope.question_unit[i].questionType = JSON.parse(c);
				var d = $scope.question_unit[i].questionUnit;
				$scope.question_unit[i].questionUnit = JSON.parse(d);
				
             	if($scope.question_unit[i].questionType.typeKey == "draganddropquestionsincolumnformat" ){
             		var dem =0;
             		$scope.question_unit[i].youranswer={};
             		for(var j = 0;j<$scope.question_unit[i].questionContents.listAnswer.length;j++)
             		{
             			if($scope.question_unit[i].questionContents.listAnswer[j].key== "column label"){
             				
             				$scope.question_unit[i].youranswer[$scope.question_unit[i].questionContents.listAnswer[j].value]= [];
             				
             			}
             		}
             			
             	}
			}
			console.log($scope.question_unit);
			$scope.unitID = unit.unitID;//take unitID for answer 
			$('.loadweb').hide();
		});
		$scope.values = {};
		$scope.audio = function(url){
			$(".audio").replaceWith( "<div class='col-md-12'><audio controls src='"+url+"'> </audio></div>" );
		};
		$scope.score =[];
	  	$scope.done = 0;
	  	$scope.flag_score = 0;
	  	$scope.check = function(questionu,value,length,index){
	  		
	  		var score=0;
	  		if(questionu.questionType.typeKey == 'choicequestions' || questionu.questionType.typeKey == 'choicequestionsselectedimage'){
	  			if(questionu.questionContents.answer[0].value == questionu.youranswer){
	  				score = 100;
	  					$scope.flag_score = 1;
	  					$scope.score_show = score;
	  			}
	  			else {
	  				score = 0;
	  				$scope.flag_score = 2;
	  				$scope.score_show = score;
	  				}
	  			questionu.score = score;
	  			$scope.score.push(questionu);
	  		}
	  		else if(questionu.questionType.typeKey == 'multiplechoicequestions'||questionu.questionType.typeKey == 'thequestionmultiplechoiceimages' )
	  		{
	  			var i,x, f;
	  			questionu.youranswer= value;
	  		
	  			for(i=0;i<questionu.questionContents.answer.length;i++){
	  				x=questionu.questionContents.answer[i].value;
	  					if(value[x])
	  						f= true;
	  					else {
	  						f =false;
	  						break;
	  					}
	  				
	  			}
	  			if(f)
	  			{
	  				$scope.flag_score = 1;
	  				$scope.score_show = 100;
	  				questionu.score = 100;
	  			$scope.score.push(questionu);
	  			}
	  			else
	  			{
	  				$scope.flag_score = 2;
	  				questionu.score = 0;
	  				$scope.score_show = 100;
	  			$scope.score.push(questionu);
	  			}
	  		}
	  		var dem =0;
	  		//questionformfillintheword
	  		if(questionu.questionType.typeKey == 'questionformfillintheword')
	  		{
	  			questionu.youranswer= value;
	  			score = 0;
	  			var dem_dung =0;
	  			for(i=0;i<questionu.questionContents.listAnswer.length;i++){
	  				if(questionu.questionContents.listAnswer[i].key== "form fill")
	  				{
	  					
	  					var b =JSON.stringify(value['field_' + i]);
	  					b=b.trim().toLowerCase();
	  					var c = JSON.stringify(questionu.questionContents.listAnswer[i].keyinput);
	  					c=c.trim().toLowerCase();
	  					if(b==c)
			  				{
			  					score =score+100;
			  					dem=dem+1;
			  				}
			  				dem_dung = dem_dung+1;
	  				}
	  				
	  			}
	  			if(dem)
	  			{
	  				$scope.score_show = score/dem_dung; 
	  				questionu.score = score/dem_dung;
	  				questionu.score = questionu.score;
	  				$scope.flag_score = 1;	
	  			}
	  			else {
	  				$scope.score_show = 0;
	  				questionu.score = 0;
	  				$scope.flag_score = 2;
	  			}
	  			$scope.score.push(questionu);
	  			
	  			
	  		}
	  		//câu hỏi dạng kéo thả.
	  		if(questionu.questionType.typeKey == 'draganddropquestionsincolumnformat'){
	  				score=0;
	  				
	  				for(i = 0;i<questionu.questionContents.answer.length;i++)
	  				{
	  					x = questionu.questionContents.answer[i].column;
	  					var y = questionu.youranswer[x];
	  					
	  					for(var j=0;j<y.length;j++)
	  					{
	  						if(questionu.questionContents.answer[i].choose == y[j].value)
	  						score=score+100;
	  						
	  					} 
	  				}
	  				if(score==0)
	  				{
	  					$scope.flag_score = 2;
	  				}else $scope.flag_score = 1;
	  				$scope.score_show = score/questionu.questionContents.answer.length;
	  				questionu.score = score/questionu.questionContents.answer.length;
	  				questionu.score =questionu.score;
	  				$scope.score.push(questionu);
	  			}
	  		
	  		// final score
	  		score = 0;
	  		$scope.finalscore = 0;
	  		for(var i=0;i<$scope.score.length;i++)
	  		{
	  			score= (score +$scope.score[i].score);
	  		}
	  		$scope.finalscore =score/$scope.score.length;	
	  		$scope.finalscore = $scope.finalscore.toFixed(2);
	  		var a=length-1;
	  		if(a== index){
	  			$http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
				var xsrf = $.param({
					questionID:$scope.unitID,
					answerContent: JSON.stringify($scope.score),
					answerScore:$scope.finalscore
				});
					$http({method:'POST',url: '/setanswer',data: xsrf,}).success(function(data){
						console.log(data);
					});
	  			}
	  		console.log($scope.finalscore,a,index);
	  		$scope.done = 1;
	  		$scope.values={};
	  	};
	  	
	  	$scope.continues = function(){
	  		$scope.flag_score = 0;
	  		$scope.done = 0;
	  		$scope.qs_index = $scope.qs_index+1;
	  		};	
	  	
  	};
  	//if()		
  	
};
// signup
function myprofileController($scope,$http,$location,$filter,$cookies){
	$http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
	var xsrf = $.param({});
		$http({method:'POST',url: '/getfulluser',data: xsrf,}).success(function(data){
			$scope.fulluser = data;
			$scope.status = status;
			console.log(data);
		});
};
// Activity
function activityController($scope,$http,$location,$filter,$cookies)
{
	$scope.Average_Score = 0;
	$http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
	var xsrf = $.param({});
		$http({method:'POST',url: '/getmyactivity',data: xsrf,}).success(function(data){
			$scope.myactivity = data;
			var x,y,z;
			for(var i=0;i<$scope.myactivity.myactivity.length;i++)
			{
				x= $scope.myactivity.myactivity[i].answerContent;
				$scope.myactivity.myactivity[i].answerContent = JSON.parse(x);
				y= $scope.myactivity.myactivity[i].answerQuestion;
				$scope.myactivity.myactivity[i].answerQuestion = JSON.parse(y);
				 z= $scope.myactivity.myactivity[i].answerUser;
				$scope.myactivity.myactivity[i].answerUser = JSON.parse(z);
				z= $scope.myactivity.myactivity[i].answerQuestion.questionAuthor;
				$scope.myactivity.myactivity[i].answerQuestion.questionAuthor = JSON.parse(z);
				z= $scope.myactivity.myactivity[i].answerQuestion.questionContents;
				$scope.myactivity.myactivity[i].answerQuestion.questionContents = JSON.parse(z);
				z= $scope.myactivity.myactivity[i].answerQuestion.questionSkill;
				$scope.myactivity.myactivity[i].answerQuestion.questionSkill = JSON.parse(z);
				z= $scope.myactivity.myactivity[i].answerQuestion.questionType;
				$scope.myactivity.myactivity[i].answerQuestion.questionType = JSON.parse(z);
				z= $scope.myactivity.myactivity[i].answerQuestion.questionUnit;
				$scope.myactivity.myactivity[i].answerQuestion.questionUnit = JSON.parse(z);
				$scope.Average_Score = $scope.Average_Score +$scope.myactivity.myactivity[i].answerScore;
			}
			$scope.Average_Score =($scope.Average_Score/$scope.myactivity.myactivity.length).toFixed(2);;
			console.log($scope.myactivity);
		});
		
};

// Archive
function archiveController($scope, FileUploader,$http,$location,$filter,$cookies)
{
	$http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
	var xsrf = $.param({});
		$http({method:'POST',url: '/getmyfile',data: xsrf,}).success(function(data){
			$scope.myfile = data;
			console.log(data);
		});
	
	//set avatar
	$scope.setavatar = function(fileID){
		$http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
		var xsrf = $.param({
			fileID:fileID,
		});
			$http({method:'POST',url: '/setavatar',data: xsrf,}).success(function(data){
				$scope.user = data.account;
				console.log($scope.user);
			});
	};
	// set files upload
	$scope.newupload = function(){
		$('#uploadercontent').modal('show');
	};
	
	$http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
	var uploader = $scope.uploader = new FileUploader({
		url: 'uploadfile',autoUpload:true
        });
		
        // FILTERS

      //  uploader.filters.push({
        //    name: 'imageFilter',
          //  fn: function(item /*{File|FileLikeObject}*/, options) {
            //    var type = '|' + item.type.slice(item.type.lastIndexOf('/') + 1) + '|';
             //   return '|jpg|png|jpeg|bmp|gif|'.indexOf(type) !== -1;
          //  }
       // });

        // CALLBACKS

        uploader.onWhenAddingFileFailed = function(item /*{File|FileLikeObject}*/, filter, options) {
            console.info('onWhenAddingFileFailed', item, filter, options);
        };
        uploader.onAfterAddingFile = function(fileItem) {
            console.info('onAfterAddingFile', fileItem);
        };
        uploader.onAfterAddingAll = function(addedFileItems) {
            console.info('onAfterAddingAll', addedFileItems);
        };
        uploader.onBeforeUploadItem = function(item) {
            console.info('onBeforeUploadItem', item);
        };
        uploader.onProgressItem = function(fileItem, progress) {
            console.info('onProgressItem', fileItem, progress);
        };
        uploader.onProgressAll = function(progress) {
            console.info('onProgressAll', progress);
        };
        uploader.onSuccessItem = function(fileItem, response, status, headers) {
            console.info('onSuccessItem', fileItem, response, status, headers);
        };
        uploader.onErrorItem = function(fileItem, response, status, headers) {
            console.info('onErrorItem', fileItem, response, status, headers);
        };
        uploader.onCancelItem = function(fileItem, response, status, headers) {
            console.info('onCancelItem', fileItem, response, status, headers);
        };
        uploader.onCompleteItem = function(fileItem, response, status, headers) {
            console.info('onCompleteItem', fileItem, response, status, headers);
            $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
			var xsrf = $.param({});
				$http({method:'POST',url: '/getmyfile',data: xsrf,}).success(function(data){
					$scope.myfile = data;
					console.log(data);
				});
        };
        uploader.onCompleteAll = function() {
            console.info('onCompleteAll');
        };

        console.info('uploader', uploader);
		
};
function discussionController($scope, FileUploader,$http,$location,$filter,$cookies)
{
	
	 var type ='';
	$scope.newupload_image = function(){
		$('#uploadercontent').modal('show');
		type = 'image';
	};
	$scope.newupload_file = function(){
		$('#uploadercontent').modal('show');
		type = 'file';
	};
	$scope.newupload_mp3 = function(){
		$('#uploadercontent').modal('show');
		type = 'mp3';
	};
	
	// load Status /////
	function loadstatus(){
		var a;
		$http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
		var xsrf = $.param({
						usr:$('body').attr('titanium'),
						authorization: $('body[authorization]').attr('authorization')
						});
		$http({method:'POST',url: '/getstatus',data: xsrf,}).success(function(data){
			$scope.allstatus = data;
			for(var i = 0; i < data.statuss.length; i++)
			{
				a = $scope.allstatus.statuss[i].status;
				$scope.allstatus.statuss[i].status = JSON.parse(a);
				a = $scope.allstatus.statuss[i].status.statusContent;
				$scope.allstatus.statuss[i].status.statusContent = JSON.parse(a);
				a = $scope.allstatus.statuss[i].comments;
				$scope.allstatus.statuss[i].comments = JSON.parse(a);
				a = $scope.allstatus.statuss[i].likestatus;
				$scope.allstatus.statuss[i].likestatus = JSON.parse(a);
				a = $scope.allstatus.statuss[i].status.statusAuthor;
				$scope.allstatus.statuss[i].status.statusAuthor = JSON.parse(a);
				for(var j= 0;j< $scope.allstatus.statuss[i].comments.commentStatus.length;j++ )
				{
					a = $scope.allstatus.statuss[i].comments.commentStatus[j].comment;
					$scope.allstatus.statuss[i].comments.commentStatus[j].comment = JSON.parse(a);
					a = $scope.allstatus.statuss[i].comments.commentStatus[j].likecomment;
					$scope.allstatus.statuss[i].comments.commentStatus[j].likecomment = JSON.parse(a);
					a = $scope.allstatus.statuss[i].comments.commentStatus[j].comment.commentContent.commentAuthor;
					$scope.allstatus.statuss[i].comments.commentStatus[j].comment.commentContent.commentAuthor = JSON.parse(a);
				}
             
			}
			console.log($scope.allstatus);
		});
	};
	loadstatus();
	// Đăng Status
	$scope.status = {};
	$scope.status.files =[];
	$scope.poststatus = function(){
		$http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
		var xsrf = $.param({status : JSON.stringify({
			'content':$scope.status.content,
			'file':$scope.status.files
		})	
		});
		$http({method:'POST',url: '/setstatus',data: xsrf,}).success(function(data){
			$scope.status = {};
			$scope.status.files =[];
			var uploader = $scope.uploader = new FileUploader({
		 autoUpload : true ,url: 'uploadfile'
        });
			loadstatus();
		});
		
	};
	// upload File

	$http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
	var uploader = $scope.uploader = new FileUploader({
		 autoUpload : true ,url: 'uploadfile'
        });
		
        // FILTERS

      // uploader.filters.push({
        //    name: 'imageFilter',
          //  fn: function(item /*{File|FileLikeObject}*/, options) {
            //    var type = '|' + item.type.slice(item.type.lastIndexOf('/') + 1) + '|';
             //   return '|jpg|png|jpeg|bmp|gif|'.indexOf(type) !== -1;
           // }
      // });

        // CALLBACKS

        uploader.onWhenAddingFileFailed = function(item /*{File|FileLikeObject}*/, filter, options) {
            console.info('onWhenAddingFileFailed', item, filter, options);
 
        };
        uploader.onAfterAddingFile = function(fileItem) {
            console.info('onAfterAddingFile', fileItem);
            
        };
        uploader.onAfterAddingAll = function(addedFileItems) {
            console.info('onAfterAddingAll', addedFileItems);
        };
        uploader.onBeforeUploadItem = function(item) {
            console.info('onBeforeUploadItem', item);
        };
        uploader.onProgressItem = function(fileItem, progress) {
            console.info('onProgressItem', fileItem, progress);
        };
        uploader.onProgressAll = function(progress) {
            console.info('onProgressAll', progress);
        };
        uploader.onSuccessItem = function(fileItem, response, status, headers) {
            console.info('onSuccessItem',response);
            var a = {'type':type,'file':response.file};
            $scope.status.files.push(a);
            $('#uploadercontent').modal('hide');
            
        };
        uploader.onErrorItem = function(fileItem, response, status, headers) {
            console.info('onErrorItem', fileItem, response, status, headers);
        };
        uploader.onCancelItem = function(fileItem, response, status, headers) {
            console.info('onCancelItem', fileItem, response, status, headers);
        };
        uploader.onCompleteItem = function(fileItem, response, status, headers) {
            console.info('onCompleteItem', fileItem, response, status, headers);
        };
        uploader.onCompleteAll = function() {
            console.info('onCompleteAll');
        };
        // comment
        $scope.submit = function(statusID) {
   
        	var a = $("#"+statusID).val();
        	$http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
			var xsrf = $.param({
				statusID : statusID,
				comment : a
			});
			$http({method:'POST',url: '/setcomment',data: xsrf,}).success(function(data){
				$http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
				var xsrf = $.param({
						usr:$('body').attr('titanium'),
						authorization: $('body[authorization]').attr('authorization')
						});
			$http({method:'POST',url: '/getstatus',data: xsrf,}).success(function(data){
			$scope.allstatus = data;
			loadstatus();
			
		});
			});
        };
        //like status
       $scope.like = function(item){
       	var xsrf = $.param({
       					statusID: item.status.statusID,
						usr:$('body').attr('titanium'),
						authorization: $('body[authorization]').attr('authorization')
						});
		$http({method:'POST',url: '/setlike',data: xsrf,}).success(function(data){
			
			loadstatus();
		});
       	
       };
       //remove like status
    $scope.removelike = function(item){
       	var xsrf = $.param({
       					statusID: item.status.statusID,
						usr:$('body').attr('titanium'),
						authorization: $('body[authorization]').attr('authorization')
						});
		$http({method:'POST',url: '/removelike',data: xsrf,}).success(function(data){
			loadstatus();
		});
       	
       };
	$scope.likeshow = function(item){
		var usr =$('body').attr('titanium');
		var a = true;
		var usrkt = -1;
		for (var i=0;i<item.likestatus.likeStatus.length;i++)
		{
			usrkt = item.likestatus.likeStatus[i].likeAuthorID;
			if( usrkt == usr)
			{
				a = false;
			}
		}
		return a;
	};
        console.info('uploader', uploader);       
};

//
function registerschoolController($scope,$http,$location,$filter,$cookies) {
	$http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
	var xsrf = $.param({
						usr:$('body').attr('titanium'),
						authorization: $('body[authorization]').attr('authorization')
						});
	$http({method: 'POST',url: '/getalluniversity',data: xsrf,}).success(function(data, status) {
		$scope.getalluniversity = data;	
		for(var i=0;i<$scope.getalluniversity.Alluniversity.length;i++)
		{
			var a = $scope.getalluniversity.Alluniversity[i].universityInfor;
			$scope.getalluniversity.Alluniversity[i].universityInfor = JSON.parse(a);
		}
		console.log($scope.getalluniversity.Alluniversity);
	});
};
//check empty object
function isEmpty(object) {
  if(object == '' || object == null || object == undefined || object == 'null'){
  	return true;
  }else{
  	return false;
  }
};

app.directive('popover', function () {
	return {
		restrict: 'AC',
		link: function (scope, element, attrs) {
			console.log(element);
			$('.selector-popover').popover('hide');
			$(element).popover({
               
                'content': function() {
                    return $compile($(element).html())(scope);
                }
            });
		}
	};
});
app.directive('tooltip', function () {
	return {
		restrict: 'AC',
		link: function (scope, element, attrs) {
			$(element).tooltip({               
                'title': function() {
                    return $compile($(element).html())(scope);
                }
            });
		}
	};
});
app.directive('enterSubmit', function () {
    return {
      restrict: 'A',
      link: function (scope, elem, attrs) {
       
        elem.bind('keydown', function(event) {
          var code = event.keyCode || event.which;
                  
          if (code === 13) {
            if (!event.shiftKey) {
              event.preventDefault();
              scope.$apply(attrs.enterSubmit);
            }
          }
        });
      }
    };
  });

