from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import *
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.generic.simple import *
from sen.usrper.models import students
# Create your views here 
def loginpage(request):
   #HttpResponse(request.message)
   return direct_to_template(request,'login.html')
def check_login(request):
   if request.method == 'POST':
      usernam = request.POST['username']
      url = "/user/" + usernam
      user = authenticate(username = request.POST['username'],password = request.POST['password'])
      if user is not None:
         if user.is_active:
            login(request,user)
            request.session['user_id'] = usernam
            request.session['req_not'] = True
            variables = RequestContext(request,{'username' : usernam,'url' : url})
            return render_to_response('homepage.html',variables)
         else:
            return HttpResponse('account disabled')
      else:
         return HttpResponse('invalid username or password')
def spage(request):
   return direct_to_template(request,'signup.html')


def signuppage(request):
   if request.method == 'POST':
      if request.POST['password']==request.POST['passworda']:
         newuser = students(name = request.POST['firstname'] + request.POST['lastname'], cemailid = request.POST['emailaddress'], phonenumber = request.POST['phonenumber'],studentid = request.POST['userid'],emailid = request.POST['userid'] + "@daiict.ac.in")  
         newuser.save()
         nwusr = User.objects.create_user(request.POST['userid'],request.POST['emailaddress'],request.POST['password'])
         newuser.is_staff= False
         nwusr.save()
         #message = "signedup sucessfully" 
         return HttpResponse('completed sucessfully')
         #return direct_to_template(request,'login.html')
      return HttpResponse('Unsuccessful')
   else:
      return HttpResponse('GET')

def logout(request):
   logout(request)
   return HttpResponse('logged_out.html')

def update_profile(request): # doubtfi=ull i dont know weather it will work or not
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
   
def user_page(request, username):
    try:
      user = User.objects.get(username=username)
    except User.DoesNotExist:
      raise Http404(u'Requested user not found.')

    if(username!= request.session['user_id']):
       return HttpResponse("you are in the wrong place")
    else:
       variables = RequestContext(request, { 'username': username })
       return render_to_response('homepage.html', variables)
