from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import *
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.generic.simple import *
from sen.usrper.models import students
# Create your views here.

def planner_view(request):
   #code for planner
   #time = "do cheesain kisi ke liya nahi rukti peshaab or nadda"
   nam=request.session['user_id']
   tim=datetime.datetime.now()
   y=tim.year
   m=tim.month
   d=tim.day
   s=tim.second
   h=tim.hour
   g=y+m+d+s+h/y-h+m
   print g
   variables = RequestContext(request,{'lect' :"todays lectures are cancelled",'time' :tim,'lnm':"aaj "+ nam +"ka lecture hai"})
   return render_to_response("planner-page.html",variables)
