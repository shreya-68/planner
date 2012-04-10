from sen.groups.models import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import *
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.generic.simple import *
#from sen.usrper.models import students
# Create your views here.
def create_group(request):    #use to create a group but there are some issues with creating a group 
   if not request.user.is_authenticated():
      return render_to_response('/login.html')
   admid =request.session['user_id']
   adm = students.objects.get(studentid = admid)
   ag=request.POST['groupname']
   #mynum=datetime.datetime.now()
   print(ag)
   print(admid)
   newgroup = group(agenda = ag,groupadmin = admid)
   newgroup.save()
   mem= groupmem(members=adm,groupid = newgroup)
   mem.save()
   return  show_group(request,newgroup.id)#render_to_response("my_groups.html")
   
def show_group(request, gid):   # THIS IS FOR SHOWING INDIVIDUAL GROUP
	if not request.user.is_authenticated():
		return render_to_response('/login.html')
	#check if user is member of group or not
	#if user is member of group then:
	try:
		grps = group.objects.get(id = gid)
		usrid = request.session['user_id']
		user = students.objects.get(studentid = usrid)
		if groupreq.objects.get(stdrqstd=user):
			req=True
		grp = RequestContext(request,{'grp' : grps})
		print (gr.agenda)
		return render_to_response("show_group.html",{grp,req})
	except :
		#msg = "You are not a member of this group"
		return render_to_response("show_group.html",request)

def delreq(request,gid):
	if not request.user.is_authenticated():
		return render_to_response('/login.html')
	group1=group.objects.filter(id = gid)
	std1=group.objects.filter(id = request.session['user_id'])
	mem=groupmem.objects.filter(stdrqstd = std1).filter(groupid=group1)
	mem.delete()
	return 	HttpResponse('completed sucessfully')
def join_group(request,gid):  #it should redirect the page from joining to home 
   if not request.user.is_authenticated():
      return render_to_response('/login.html')
   membid =request.session['user_id']
   memb = students.objects.get(studentid = membid)
   grps = group.objects.get(id = gid)
   opr=groupreq.objects.filter(stdrqstd = memb).all().filter(grp=grps)
   #opr=r.get(stdrqstd = memb)
   if opr is None:
	      message="you are already a part of this group"
   else:
		mem= groupmem(members=memb,groupid =grps)
		mem.save()
		opr.delete()
		message="congo"   
   #groupreq.objects.filter(id = gid).filter(stdrqstd = memb).delete()
   return HttpResponse(message,gid)
def delete_mem_group(request):   #doubtfull   THE WHOLE FUNCTION IS NOT CHECKED  
   if not request.user.is_authenticated():
      return render_to_response('/login.html')   
   admid =request.session['user_id']
   memid = request.POST['member']
   grpr=group.objects.filter(id=gid)
   adm=grpr.groupadmin
   grp = groupmem.objects.filter(members=memid).filter(groupid=grpr)
   if(admid == adm):
      grp = group.objects.get(members = mem)
      grp.delete()
      return HttpResponse('comleted')
   else:
      return HttpResponse('Unsuccessful')
def get_members(request, gid):
       if not request.user.is_authenticated():
             return render_to_response('/login.html')
       grpob = groupmem.objects.get(id=gid) # NEEDS to BE UPDATE
       return render_to_response("tabs/tab3.html",grpob)
   #else :
       #return Httpresponse('you cannnot view this page')
def change_admin_to(request,gid):
   if not request.user.is_authenticated():
         return render_to_response('/login.html')
   chadminid = request.session['user_id']#group.objects.get(request.POST['groupid'])
   nwadminid = request.POST['member']
   admin=group.objects.get(id=gid)
   if chadminid == admin.groupadmin:
      nwad = students.objects.get(nwadmin)
      admin.objects.all().update(groupadmin = nwadminid)
      chadmin.save()
   return HttpResponse('adminchanged')
def gevent_create(request,gid):           #need to check this function
   if not request.user.is_authenticated():
         return render_to_response('/login.html')
   postee = request.session['user_id']
   noti =request.POST['noti']
   ob = groupupdates(event = noti, updtby = postee)
   ob.grpid = group.objects.get(id=gid)
   ob.save()
   return HttpResponse['entered update']
def delete_group(request,gid):
   if not request.user.is_authenticated():
         return render_to_response('/login.html')       
   grp = group.objects.filter(id=gid)
   adm=grp.groupadmin
   if adm==request.session['user_id']:
      grp = group.objects.filter(id=gid)
      groupmem.objects.filter(groupid=grp).delete()
      grp.delete()
      return HttpResponse('completed')
   else:
	   return HttpResponse('not done')
def all_events(request):
   if not request.user.is_authenticated():
         return render_to_response('/login.html')
   grpid = request.POST['grpid']
   noti = groupupdates.objects.get(id = grpid)
   return HttpResponse(noti)
def request_group(request,gid):      # ADDS A REQUEST IN THE REQUEST TABLE
   if not request.user.is_authenticated():
         return render_to_response('/login.html')
   uname=request.POST['username']
   grid = gid		#request.POST['grpid']
   grp = group.objects.get(id = grid)
   groupt=groupmem.objects.get(groupid=grp)
   std = students.objects.get(studentid = uname)
   if groupt.members.all().filter(members = std):
	   return Httpresponse("you are already in the group")
   else:
	   gr=groupreq(id = gid)
	   gr.stdrqstd = std
	   gr.save()
	   return Httpresopnse("sucessful")
def show_grp(request):						##  THIS IS FOR SHOWING ALL THE GROUPS		
    if not request.user.is_authenticated():
           return render_to_response('/login.html')
    sid=request.session['user_id']
    user=students.objects.get(studentid = sid)
    #g=group.objects.get(id = 1)
    try:
		allgroups = groupmem.objects.filter(members = user)
		#for grp in allgroups.all():
		#	print(grp.groupid.agenda) 
		reqgroup = groupreq.objects.filter(stdrqstd = user)    #is of requesttype
		#print(reqgroup)
		for grps in reqgroup.all():
		   print(grps.grp.agenda)
		var = RequestContext(request,{'allgroups': allgroups,'reqgroup':reqgroup})
		return render_to_response('my_groups.html',var)
    except groupmem.DoesNotExist:
        var = RequestContext(request,{'allgroups': allgroups})
        return render_to_response('my_groups.html',var)
    except groupreq.DoesNotExist:
        var = RequestContext(request,{'allgroups': allgroups})
        return render_to_response('my_groups.html',var)
