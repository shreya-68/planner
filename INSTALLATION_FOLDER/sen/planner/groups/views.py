
from django.contrib.auth.decorators import login_required 
from groups.models import *
from event.models import *
from event.forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import *
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.generic.simple import *

@login_required(login_url = '/login/')
def create_group(request):
    """
    requesting user creates a group
    """
    if request.method == 'POST':
        admin_id = request.user.username
        admin = students.objects.get(studentid = admin_id)
        gr_agenda = request.POST['groupname']
        new_group = group(agenda = gr_agenda, groupadmin = admin_id)
        new_group.save()
        member = groupmem(member = admin, grp = new_group)
        member.save()
        return show_group(request, new_group.id) 
    else:
        return render_to_response('groups/create_group.html')

@login_required(login_url = '/login/')
def show_group(request, gid = None):
    """
    displaying page of each group.
    """
    if gid == None:
        print 'hi'
        print request.user.username
        member = students.objects.get(studentid = request.user.username)
        all_groups = groupmem.objects.filter(member = member)
        requested_groups = groupreq.objects.filter(member = member)
        var = RequestContext(request, {'all_groups': all_groups, 'requested_groups': requested_groups})
        return render_to_response('groups/groups.html', var)

    else:    
        current_group = group.objects.get(id = gid)
        if current_group:
            group_members = groupmem.objects.filter(grp = current_group)
            member = students.objects.get(studentid = request.user.username)
            requested_members = groupreq.objects.filter(grp = current_group)
            all_groups = groupmem.objects.filter(member = member)
            requested_groups = groupreq.objects.filter(member = member)
            all_members = members(gid)
            if current_group.groupadmin == member.studentid:
                admin = True
            else:
                admin = False
            for each in group_members:
                if each.member == member:
                    request_pending = False
                    return render_to_response('groups/show_group.html', {'current_group': current_group, 'all_groups': all_groups, 'members': all_members, 'request_pending': request_pending, 'requested_groups': requested_groups, 'admin': admin})
            for each in requested_members:
                if each.member == member:
                    request_pending = True
                    print request_pending
                    return render_to_response('groups/show_group.html', {'current_group': current_group, 'all_groups': all_groups, 'members': all_members, 'request_pending': request_pending, 'requested_groups': requested_groups, 'admin': admin})
            msg = "You are not a member of this group hence you cannot view this page"
            msg_type = 'warning'
            return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})
        else:
            msg = "This group does not exist"
            msg_type = 'error'
            return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})


def members(gid):
    members = groupmem.objects.filter(grp__id = gid)
    return members

@login_required(login_url = '/login/')
def get_members(request, gid):
    members = groupmem.objects.filter(grp__id = gid)
    return render_to_response('groups/show_members.html', {'members': members, 'gid': gid})

@login_required(login_url = '/login/')
def delete_members(request, gid):
    members = groupmem.objects.filter(grp__id = gid)
    return render_to_response('groups/delete_members.html', {'members': members, 'gid': gid})

@login_required(login_url = '/login/')
def delete_member(request, gid, mid):
    this_grp = group.objects.get(id = gid)
    if int(request.user.username) == this_grp.groupadmin:
           row = groupmem.objects.filter(member__studentid = mid).filter(grp__id = gid)
           if row:
               row.delete()
               msg = "Group member deleted successfully"
               msg_type = 'success'
               return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})
           else:
            msg = "Group member doesn't exist in this group"
            msg_type = 'error'
            return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})
    else:
        print this_grp.groupadmin
        msg = "You do not have permission to delete any member of this group"
        msg_type = 'warning'
        return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})


@login_required(login_url = '/login/')
def delete_group(request, gid):
    grp = group.objects.get(id = gid)
    admin = grp.groupadmin
    print admin
    print request.user.username
    if int(admin) == int(request.user.username):
        print 'hi'
        groupmem.objects.filter(grp = grp).delete()
        groupreq.objects.filter(grp = grp).delete()
        grp.delete()
        msg = "You have successfully deleted this group"
        msg_type = 'success'
        return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})
    else:
        msg = "You do not have permission to delete this group"
        msg_type = 'warning'
        return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})

@login_required(login_url = '/login/')
def edit_group(request, gid):
    grp = group.objects.get( id = gid)
    if grp.groupadmin == int(request.user.username):
        return render_to_response('groups/edit_group.html', {'gid': gid})
    else:
        msg = "You do not have permission to edit this group"
        msg_type = 'warning'
        return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})

@login_required(login_url = '/login/')
def send_request(request, gid):
    """
    send request to user
    """
    if request.method == 'POST':
        if int(request.user.username) == int(group.objects.get(id = gid).groupadmin):
            grp = group.objects.get(id = gid)
            user = students.objects.get(studentid = request.POST['username'])
            members = groupmem.objects.get(grp = grp)
            #if !members.member.all().filter(member = user):
            new_request = groupreq(grp = grp, member = user)
            new_request.save()
            msg = "You have successfully sent request to a member to join this group"
            msg_type = 'success'
            return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})
            #else:
            #    msg = "Member already exists in this group"
            #    msg_type = 'error'
            #    return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})
        else:
            msg = "You cannot add a member to this group"
            msg_type = 'warning'
            return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})
    else:
        return render_to_response('groups/send_request.html',{'gid':gid})



@login_required(login_url = '/login/')
def join_group(request, gid):
    user = students.objects.get(studentid = int(request.user.username))
    this_group = group.objects.get(id = gid)
    group_request = groupreq.objects.filter(member = user).filter(grp = this_group)
    if group_request:
        new_member = groupmem(member = user, grp = this_group)
        new_member.save()
        msg = "You have successfully joined this group"
        msg_type = 'success'
        return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})
    else:
        msg = "You do not have permission to join this group"
        msg_type = 'warning'
        return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})


@login_required(login_url = '/login/')
def delete_request(request, gid):
    row = groupreq.objects.filter(member__studentid = request.user.username).filter(grp__id = gid)
    row.delete()
    msg = "Request removed"
    msg_type = 'success'
    return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})


@login_required(login_url = '/login/')
def add_event(request, gid):
    grp = group.objects.get( id = gid)
    if grp.groupadmin == int(request.user.username):
        if request.method == 'POST':
            print 'hi'
            form = PrePrepForm(request.POST)
            if form.is_valid():
                print 'OO'
                pre_prep = form.save(commit = False)
                eventform = EventForm(request.POST)
                if eventform.is_valid():
                    print eventform
                    pre_prep.save()
                    eventform.save(commit = False)
                    eventform.user = request.user
                    eventform.start_time = '2/3/2012 00:00:00'
                    eventform.end_time = '2/3/2012 21:00:00'
                    eventform.pre_prep = pre_prep
                    new_event = eventform.save()
                    eid = request.POST['event_type']
                    event_type = Event_Type.objects.get(id = eid).get_event_type_display()
                    if event_type == 'Lecture':
                        print 'Lecture'
                        course = Course.objects.get(id = request.POST['course'])
                        et = Event_Type.objects.get(id = 1)
                        lecture = Lecture(course = course, Type = et, event = new_event, id = new_event.id)
                        lecture.save()
                    elif event_type == 'Project':
                        print 'Project'
                        course = Course.objects.get(id = request.POST['course'])
                        et = Event_Type.objects.get(id = 2)
                        project = Project(course = course, Type = et, event = new_event, id = new_event.id) 
                        project.save()
                    elif event_type == 'Exam':
                        print 'Exam'
                        course = Course.objects.get(id = request.POST['course'])
                        et = Event_Type.objects.get(id = 3)
                        exam = Exam(course = course, Type = et, event = new_event, id = new_event.id) 
                        exam.save()
                    elif event_type == 'Sport':
                        et = Event_Type.objects.get(id = 4)
                        sport = Sport(Type = et, event = new_event, id = new_event.id) 
                        sport.save()
                    elif event_type == 'Club':
                        et = Event_Type.objects.get(id = 5)
                        club = Club(club_name = request.POST['club_name'], Type = et, event = new_event, id = new_event.id) 
                        club.save()
                    else:
                        et = Event_Type.objects.get(id = 6)
                        other = Other(Type = et, event = new_event, id = new_event.id)
                        other.save()
                    group_event = groupevent(grp = grp, event = new_event.id)
                    group_event.save()

                    #members = groupmem.objects.filter(grp = grp)
                    #for member in members:
                    #    event_request = groupeventrequests(group_event = group_event, member = member)
                    print 'success'
                    msg = "Event created successfully"
                    msg_type = 'success'
                    return render_to_response('notify/notify.html', {'msg': msg, 'msg_type':msg_type})
            else:
                print form.errors
                return HttpResponse("Failure")
        else:
            form = PrePrepForm()
        event_type = Event_Type.objects.all()
        courses = Course.objects.all()
        eventform = EventForm(instance = Pre_prep())
        return render_to_response("groups/add_event.html", {'form':form, 'eventform': eventform, 'courses': courses, 'event_type': event_type, 'gid': gid
                        }, context_instance=RequestContext(request))
    else:
        msg = "You do not have permission to edit this group"
        msg_type = 'warning'
        return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})
   

@login_required(login_url = '/login/')
def show_events(request, gid):
    grp = group.objects.get(id = gid)
    members = groupmem.objects.filter(grp = grp)
    member = students.objects.get(studentid = request.user.username)
    if member in members.member:
    	events = groupevent.objects.filter(grp = grp)
    	group_events = []
        for e in events:
            for table in (Lecture, Club, Project, Exam, Sport, Other):
    	        row = table.objects.get(id = e.event)
                if row:
                	group_events.append(row)
        return render_to_response('groups/group_events.html', {'gid': gid, 'group_events': group_events})
                	

    
