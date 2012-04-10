from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import *
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.generic.simple import *
from usrper.models import *
from groups.models import *
from event.models import *
from event.views import *
import datetime
import calendar
# Create your views here.

month_names = "January February March April May June July August September October November December"
month_names = month_names.split()

def loginpage(request):
   #HttpResponse(request.message)
   #if not request.user.is_authenticated():
    return render_to_response('login/login.html',context_instance = RequestContext(request) )
   #else:
          #return HttpResponse('User is logged in logout first to login again')

#check that username exists in students table
def check_login(request):
    if request.method == 'POST':
        usernam = request.POST['username']
        print usernam
        registered_members = students.objects.all()
        for member in registered_members:
            print 'hello'
            if int(usernam) == member.studentid:
                print 'hi'
                url = "/user/" + usernam
                user = authenticate(username = request.POST['username'],password = request.POST['password'])
                print user
                if user is not None:
                    print 'xxxx'
                    if user.is_active:
                        login(request,user)
                        request.session['user_id'] = usernam
                        date = datetime.date.today()
                        user = students.objects.get(studentid = int(request.user.username))
                        user_edit = UserEdit.objects.get(user = user)
                        if user_edit.edit == True:
                        	edit = False
                        else:
                        	edit = True
                        variables = RequestContext(request,{'username' : usernam,'url' : url, 'date': date, 'month_name' : month_names[date.month - 1], 'edit': edit })
                        return render_to_response('login/homepage.html',variables)
                    else:
                        msg = 'account disabled'
                        msg_type = 'info'
                        return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})
                msg = 'Invalid username or password'
                msg_type = 'warning'
                return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})
        msg = 'Invalid username or password'
        msg_type = 'warning'
        return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})
#        else:

def spage(request):
   #if not request.user.is_authenticated():
    return render_to_response('login/signup.html', context_instance = RequestContext(request))
   #else:
          #return render_to_response('login/logout.html')
#HttpResponse('User is logged in logout first to signup again')


def signuppage(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            print '1'
            numb = len(request.POST['phonenumber'])
            sid = len(request.POST['studentid'])
            if numb == 10 and sid == 9:
                print 2
                pwd = len(request.POST['password'])
                if pwd >= 6:
                    if request.POST['password']==request.POST['passworda']:
                        print 'confirm'
                        user = form.save(commit = False)
                        user.emailid = str(user.studentid) + "@daiict.ac.in"
                        user.save()
                        new_user = User.objects.create_user(request.POST['studentid'], user.emailid, request.POST['password'])
                        print new_user.username
                        new_user.is_staff= False
                        new_user.save()
                        user_edit = UserEdit(user = user, edit = False)
                        user_edit.save()
                        return HttpResponseRedirect('/login/')
                    return HttpResponse('Passwords did not match')
                else:
                    return HttpResponse("password has to be minimum 6 characters")
            elif numb == 10:
                print 3
                msg = "ID has to be of size 9"
                msg_type = "warning"
                return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})
            elif sid == 9:
                print 4
                return HttpResponse("Enter valid phone number")
            else:
                print 5
                return HttpResponse('Enter valid phone number and id')
        else:
            print form.errors
            return render_to_response('notify/errorlist.html', {'form': form}, context_instance = RequestContext(request))
    else:
        form = UserForm()
        return render_to_response('login/signup.html', {'form': form}, context_instance = RequestContext(request))

def edit_courses(request):
    if request.method == 'POST':
        user = students.objects.get(studentid = int(request.user.username))
        if request.POST['course_1'] != 'None':
        	course = Course.objects.get(id = request.POST['course_1'])
        	new_usercourse = UserCourses( user = user, course = course)
        	new_usercourse.save()
        if request.POST['course_2'] != 'None':
        	course = Course.objects.get(id = request.POST['course_2'])
        	new_usercourse = UserCourses( user = user, course = course)
        	new_usercourse.save()
        if request.POST['course_3'] != 'None':
        	course = Course.objects.get(id = request.POST['course_3'])
        	new_usercourse = UserCourses( user = user, course = course)
        	new_usercourse.save()
        if request.POST['course_4'] != 'None':
        	course = Course.objects.get(id = request.POST['course_4'])
        	new_usercourse = UserCourses( user = user, course = course)
        	new_usercourse.save()
        if request.POST['course_5'] != 'None':
        	course = Course.objects.get(id = request.POST['course_5'])
        	new_usercourse = UserCourses( user = user, course = course)
        	new_usercourse.save()
        if request.POST['course_6'] != 'None':
        	course = Course.objects.get(id = request.POST['course_6'])
        	new_usercourse = UserCourses( user = user, course = course)
        	new_usercourse.save()
        year = datetime.datetime.now().year
        print year
        cal = calendar.Calendar()
        for month in range(1,6): 
            month_days = cal.itermonthdays(year, month)
            for day in month_days:
                if day:
                    this_date = datetime.date(int(year), int(month), int(day))
                    add_lecture_event(request, this_date)
        edit = UserEdit.objects.get(user = user)
        edit.edit = True
        edit.save()
        return HttpResponseRedirect('/profile/')
    else:
        courses = Course.objects.all()
        user = students.objects.get(studentid = int(request.user.username))
        edit = UserEdit.objects.get(user = user)
        if edit.edit == True:
        	return HttpResponseRedirect('/home/')
        return render_to_response('login/edit_courses.html', {'courses': courses}, context_instance = RequestContext(request))

def view_profile(request):
    user = students.objects.get(studentid = int(request.user.username))
    user_courses = UserCourses.objects.filter( user = user)
    user_groups = groupmem.objects.filter(member = user)
    if user.sleephours == None:
        return render_to_response('login/show_profile.html', {'user': user, 'user_courses': user_courses, 'user_groups': user_groups}, context_instance = RequestContext(request)) 
    sleep = user.sleephours.time()
    lunch = user.lunchtime.time()
    dinner = user.dinnertime.time()
    return render_to_response('login/show_profile.html', {'user': user, 'sleep': sleep, 'lunch': lunch, 'dinner': dinner, 'user_courses': user_courses, 'user_groups': user_groups}, context_instance = RequestContext(request)) 


def create_profile(request):
    if request.method == 'POST':
        user = students.objects.get(studentid = int(request.user.username))
        form = ProfileForm(request.POST, instance = user)
        if form.is_valid():
            print '1'
            form.save()
            return HttpResponseRedirect('/home/')
        else:
            return render_to_response('notify/errorlist.html', {'form': form})
    else:
        date = datetime.date.today()
        day = date.day
        month = date.month
        year = date.year
        date = str(month)+'/'+str(day)+'/'+str(year)
        courses = Course.objects.all()
        user = students.objects.get(studentid = int(request.user.username))
        form = ProfileForm()
        return render_to_response('login/create_profile.html', {'form': form, 'date': date, 'courses': courses, 'user':user}, context_instance = RequestContext(request))

def log_out(request):
    logout(request)
    return HttpResponseRedirect('/login/')

#@login_required(login_url = '/login/')
#def home(request,usernam):
#    if request.user.username == usernam:
#        try:
#            user = User.objects.get(username=usernam)
#        except User.DoesNotExist:
#            raise Http404(u'Requested user not found.')
#        print(usernam)
#        variables=RequestContext(request,{'username' : usernam})
#        return render_to_response('mainpage.html',variables)
#    else:
#        HttpResponse("You cant access this page")
#   return direct_to_template('homepage.html')    # homepage of the user it has  


   
@login_required(login_url = '/login/')
def user_page(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404(u'Requested user not found.')

    if(username!= request.session['user_id']):
        return HttpResponse("you are in the wrong place")
    else:
        variables = RequestContext(request, { 'username': username })
        return render_to_response('login/homepage.html', variables)

@login_required(login_url = '/login/')
def home(request):
    try:
        user = students.objects.get(studentid = int(request.user.username))
        if user:
            date = datetime.date.today()
            user_edit = UserEdit.objects.get(user = user)
            if user_edit.edit == True:
            	edit = False
            else:
            	edit = True
            variables = RequestContext(request, { 'username': request.user.username, 'date': date,'edit': edit, 'month_name': month_names[date.month -1] })
            return render_to_response('login/homepage.html', variables)
        else:
            return HttpResponseRedirect('/login/')
    except:
        return HttpResponseRedirect('/login/')

