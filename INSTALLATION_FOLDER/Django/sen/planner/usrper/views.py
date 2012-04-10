from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import *
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.generic.simple import *
from usrper.models import students
# Create your views here.

def loginpage(request):
   #HttpResponse(request.message)
   #if not request.user.is_authenticated():
    return direct_to_template(request,'login/login.html')
   #else:
          #return HttpResponse('User is logged in logout first to login again')

def check_login(request):
    if request.method == 'POST':
        usernam = request.POST['username']
        url = "/user/" + usernam
        user = authenticate(username = request.POST['username'],password = request.POST['password'])
        if user is not None:
            if user.is_active:
                login(request,user)
                request.session['user_id'] = usernam
                variables = RequestContext(request,{'username' : usernam,'url' : url})
                return render_to_response('login/homepage.html',variables)
            else:
                msg = 'account disabled'
                msg_type = 'info'
                return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})

        msg = 'Invalid username or password'
        msg_type = 'warning'
        return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})
#        else:

def spage(request):
   #if not request.user.is_authenticated():
    return direct_to_template(request,'login/signup.html')
   #else:
          #return render_to_response('login/logout.html')
#HttpResponse('User is logged in logout first to signup again')


def signuppage(request):
    if request.method == 'POST':
        if request.POST['password']==request.POST['passworda']:
            newuser = students(name = request.POST['firstname'] + request.POST['lastname'], cemailid = request.POST['emailaddress'], phonenumber = request.POST['phonenumber'],studentid = request.POST['userid'],emailid = request.POST['userid'] + "@daiict.ac.in")  
            newuser.save()
            nwusr = User.objects.create_user(request.POST['userid'],request.POST['emailaddress'],request.POST['password'])
            newuser.is_staff= False
            nwusr.save()
            return HttpResponse('completed sucessfully')
        return HttpResponse('Unsuccessful')
    else:
        return HttpResponse('GET')

def log_out(request):
    logout(request)
    return HttpResponse('login/logged_out.html')

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

            
        

def update_profile(request): # doubtfull i dont know weather it will work or not
    myid = request.session['user_id']
    Name = request.POST['nam']
    Emailid = request.POST['email']
    Roomno = request.POST['room']
    Phonenumber = request.POST['phone']
    Sleephours = request.POST['sleephou']
    Lunchtime = request.POST['lunch']
    Dinnertime = request.POST['dintime']
    Usualwakingtime = request.POST['wakehour']
    Hobbies = request.POST['hobbies']
    Cpi = request.POST['cpi']
    currsem = request.POST['currentsem']
    year =request.POST['year']
    Cemailid =request.POST['cemailid']
    sas = students.objects.filter(studentid = myid).update(name = Name,emailid = Emailid,roomno = Roomno,phonenumber = Phonenumber,sleephours =Sleephours,lunchtime=Lunchtime,dinnertime=Dinnertime,usualwakingtime=Usualwakingtime,hobbies=Hobbies,cpi=Cpi,cursem=currsem,Year=year,cemailid=Cemailid)
    sas.save()
    return HttpResponse(sas)
   
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
    user = students.objects.get(studentid = int(request.user.username))
    if user:
        variables = RequestContext(request, { 'username': request.user.username })
        return render_to_response('login/homepage.html', variables)
    else:
        HttpResponse("Requested user not found")

