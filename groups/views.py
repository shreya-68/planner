
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
from usrper.models import *
from forum.views import *
import urllib
import urllib2

@login_required(login_url = '/login/')
def create_group(request):
    """
    requesting user creates a group
    """
    if request.method == 'POST':
        admin_id = request.user.username
        admin = students.objects.get(studentid = admin_id)
        gr_agenda = request.POST['groupname']
        forum = Forum(title = gr_agenda, category = 'Closed')
        forum.save()
        new_group = group(agenda = gr_agenda, groupadmin = admin_id, forum = forum)
        new_group.save()
        member = groupmem(member = admin, grp = new_group)
        member.save()
        url = '/groups/' + str(new_group.id) + '/'
        return HttpResponseRedirect(url) 
    else:
        return render_to_response('groups/create_group.html', context_instance=RequestContext(request))

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
        if len(all_groups) == 0:
            groups_exist = False
        else:
            groups_exist = True
        requested_groups = groupreq.objects.filter(member = member)
        if len(requested_groups) == 0:
            requested_groups_exist = False
        else:
            requested_groups_exist = True
        var = RequestContext(request, {'all_groups': all_groups, 'requested_groups': requested_groups, 'groups_exist': groups_exist, 'requested_groups_exist': requested_groups_exist})
        return render_to_response('groups/groups.html', var)

    else:    
        try:
            current_group = group.objects.get(id = gid)
            print 'yes'
            group_members = groupmem.objects.filter(grp = current_group)
            member = students.objects.get(studentid = request.user.username)
            requested_members = groupreq.objects.filter(grp = current_group)
            all_groups = groupmem.objects.filter(member = member)
            if all_groups.exists():
                groups_exist = True
            else:
                groups_exist = False
            requested_groups = groupreq.objects.filter(member = member)
            if requested_groups.exists():
                requested_groups_exist = True
            else:
                requested_groups_exist = False
            all_members = members(gid)
            if current_group.groupadmin == member.studentid:
                admin = True
            else:
                admin = False
            for each in group_members:
                if each.member == member:
                    request_pending = False
                    return render_to_response('groups/show_group.html', {'current_group': current_group, 'all_groups': all_groups, 'members': all_members, 'request_pending': request_pending, 'requested_groups': requested_groups, 'admin': admin, 'groups_exist': groups_exist, 'requested_groups_exist': requested_groups_exist}, context_instance=RequestContext(request))
            for each in requested_members:
                if each.member == member:
                    request_pending = True
                    print request_pending
                    return render_to_response('groups/show_group.html', {'current_group': current_group, 'all_groups': all_groups, 'members': all_members, 'request_pending': request_pending, 'requested_groups': requested_groups, 'admin': admin})
            msg = "You are not a member of this group hence you cannot view this page"
            msg_type = 'warning'
            return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})
        except:
            print 'hi'
            msg = "This group does not exist"
            msg_type = 'error'
            return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})

def members(gid):
    members = groupmem.objects.filter(grp__id = gid)
    return members

@login_required(login_url = '/login/')
def get_members(request, gid):
    try:
        members = groupmem.objects.filter(grp__id = gid)
        grp = group.objects.get(id = gid)
        if int(request.user.username) == grp.groupadmin:
            admin = True
        else:
            admin = False
        return render_to_response('groups/show_members.html', {'members': members, 'gid': gid, 'admin': admin}, context_instance=RequestContext(request))
    except:
        msg = "This group does not exist"
        msg_type = 'error'
        return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})

@login_required(login_url = '/login/')
def delete_members(request, gid):
    members = groupmem.objects.filter(grp__id = gid)
    grp = group.objects.get(id = gid)
    if int(request.user.username) == grp.groupadmin:
        admin = True
        return render_to_response('groups/show_members.html', {'members': members, 'gid': gid, 'admin': admin}, context_instance=RequestContext(request))
    else:
        msg = "You do not have permission to delete any member of this group"
        msg_type = 'warning'
        return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})

@login_required(login_url = '/login/')
def delete_member(request, gid, mid):
    try:
        this_grp = group.objects.get(id = gid)
        if this_grp.groupadmin == mid:
            msg = "You do not have permission to delete yourself from this group. Delete the group first."
            msg_type = 'warning'
            return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})
        else:     
            if int(request.user.username) == this_grp.groupadmin or int(request.user.username) == mid:
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
    except:
        msg = "This group does not exist"
        msg_type = 'error'
        return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})



@login_required(login_url = '/login/')
def delete_group(request, gid):
    try:
        grp = group.objects.get(id = gid)
        admin = grp.groupadmin
        print admin
        print request.user.username
        if int(admin) == int(request.user.username):
            print 'hi'
            groupmem.objects.filter(grp = grp).delete()
            groupreq.objects.filter(grp = grp).delete()
            grp.forum()
            grp.delete()
            msg = "You have successfully deleted this group"
            msg_type = 'success'
            return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})
        else:
            msg = "You do not have permission to delete this group"
            msg_type = 'warning'
            return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})
    except:
        msg = "This group does not exist"
        msg_type = 'error'
        return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})

@login_required(login_url = '/login/')
def edit_group(request, gid):
    try:
        grp = group.objects.get( id = gid)
        if grp.groupadmin == int(request.user.username):
            return render_to_response('groups/edit_group.html', {'gid': gid, 'grp': grp}, context_instance=RequestContext(request))
        else:
            msg = "You do not have permission to edit this group"
            msg_type = 'warning'
            return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})
    except:
        msg = "This group does not exist"
        msg_type = 'error'
        return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})

@login_required(login_url = '/login/')
def send_request(request, gid):
    """
    send request to user
    """
    if request.method == 'POST':
        if int(request.user.username) == int(group.objects.get(id = gid).groupadmin):
            print 1
            try:
                grp = group.objects.get(id = gid)
            except:
                msg = "This group does not exist"
                msg_type = 'error'
                return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})
            try:
                user = students.objects.get(studentid = request.POST['username'])
            except:
                msg = "There is no user with this username. Enter again"
                msg_type = 'warning'
                return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})
            members = groupmem.objects.filter(grp = grp)
            for member in members:
                if user == member.member:
                    msg = "Member already exists in this group"
                    msg_type = 'error'
                    return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})
            requested_users = groupreq.objects.filter(grp = grp)
            for each in requested_users:
                print 'pending'
                if each.member == user:
                    msg = "Request already pending"
                    msg_type = 'warning'
                    return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})
            new_request = groupreq(grp = grp, member = user)
            new_request.save()
            print 'sent'
            msg = "You have successfully sent request to a member to join this group"
            msg_type = 'success'
            return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})
        else:
            msg = "You cannot add a member to this group"
            msg_type = 'warning'
            return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})
    else:
        return render_to_response('groups/send_request.html',{'gid':gid}, context_instance=RequestContext(request))



@login_required(login_url = '/login/')
def join_group(request, gid):
    user = students.objects.get(studentid = int(request.user.username))
    this_group = group.objects.get(id = gid)
    group_request = groupreq.objects.filter(member = user).filter(grp = this_group)
    if group_request:
        new_member = groupmem(member = user, grp = this_group)
        new_member.save()
        group_request.delete()
        msg = "You have successfully joined this group"
        msg_type = 'success'
        return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})
    else:
        msg = "You do not have permission to join this group"
        msg_type = 'warning'
        return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})


@login_required(login_url = '/login/')
def delete_request(request, gid):
    try:
        row = groupreq.objects.filter(member__studentid = int(request.user.username)).filter(grp__id = gid)
        row.delete()
        msg = "Request removed"
        msg_type = 'success'
        return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})
    except:
        msg = "No request pending"
        msg_type = 'warning'
        return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})

def Datetime(date):
    Date = str(date.date())
    year,month,day = Date.split('-')
    Standard_Date = day+'-'+month+'-'+year
    Time = str(date.time())
    hour,minute,seconds = Time.split(':')
    Reminding_Hour = str(int(hour)-1)
    Standard_Time = Reminding_Hour+'-'+minute
    reminding_date = Standard_Date+'-'+Standard_Time
    return reminding_date

@login_required(login_url = '/login/')
def add_event(request, gid):
    grp = group.objects.get( id = gid)
    if grp.groupadmin == int(request.user.username):
        if request.method == 'POST':
            eventform = EventForm(request.POST)
            if eventform.is_valid():
                print eventform
                new_event = eventform.save(commit = False)
                print new_event.datetime
                print new_event.datetime > datetime.datetime.now()
                if new_event.datetime > datetime.datetime.now():
                    print request.user
                    print new_event.pp
                    new_event.user = request.user 
                    #eventform.start_time = '2/3/2012 00:00:00'
                    #eventform.end_time = '2/3/2012 21:00:00'
                    new_event.save()
                    print new_event.id
                    members = groupmem.objects.filter(grp = grp)
                    for member in members:
                        usr = User.objects.get(username = member.member.studentid)
                        new_event.pk = None
                        new_event.user = usr
                        new_event.save()
                        print new_event.id
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
                    user = students.objects.get(studentid = int(request.user.username))
                    group_event = groupevent(grp = grp, event = new_event.id, posted_By = user)
                    group_event.save()
                    
                    Member_SET = groupmem.objects.all().filter(grp=grp)
                    #Event_SET = groupevent.objects.all().filter(grp=grp)
                    for member in Member_SET:
                        usr = member.member
                        call = usr.phonenumber
                        note = Event.objects.get(id = new_event.id)
                        note_time = str(note.datetime)
                        note_name = note.name
                        notify = note_time+' '+note_name
                        message = {'username':'Amar', 'api_password':'4de4cegbv5sjcaj3e', 'sender':'test', 'to':call, 'message':notify, 'priority':2} 
                        parameter = urllib.urlencode(message)
                        print parameter
                        if note.remind:
                            time = Datetime(note.datetime)
                            print time
                            message2 = {'username':'Amar', 'api_password':'4de4cegbv5sjcaj3e', 'sender':'test', 'to':call, 'message':'hello', 'shtime':time, 'priority':2}
                            reminding_parameter = urllib.urlencode(message2)
                            remind_req = urllib2.Request(url='http://bulksms.gateway4sms.com/pushsms.php?',data = reminding_parameter)
                            p = urllib2.urlopen(remind_req)
                            print p.read()
                        req = urllib2.Request(url='http://bulksms.gateway4sms.com/pushsms.php?',data = parameter)
                        f = urllib2.urlopen(req)
                        print f.read()
                        url = '/groups/events/' + str(gid) + '/'
                    return HttpResponseRedirect(url)
                else:
                    return HttpResponse('Event has to occur after today\'s date.')
            else:
                return render_to_response('notify/errorlist.html', {'eventform': eventform})
        else:
            date = datetime.date.today()
            day = date.day
            month = date.month
            year = date.year
            date = str(month)+'/'+str(day)+'/'+str(year)
            event_type = Event_Type.objects.all()
            courses = Course.objects.all()
            eventform = EventForm(instance = Pre_prep())
            return render_to_response("groups/add_event.html", {'eventform': eventform, 'courses': courses, 'event_type': event_type, 'gid': gid, 'date': date }, context_instance=RequestContext(request))
    else:
        msg = "You do not have permission to edit this group"
        msg_type = 'warning'
        return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})
   

@login_required(login_url = '/login/')
def delete_event(request, eid):
    """Delete an event with pk"""

    for table in (Lecture, Club, Project, Exam, Sport, Other):
        x = 0
        try:
            row = table.objects.get(id = eid)
        except:
            print 1
            x = 1
            pass
        if x == 0:
            print 0
            print eid
            #if row.event.user.username == request.user.username:
            group_event = groupevent.objects.get(event = eid)
            grp = group_event.grp
            Member_SET = groupmem.objects.filter(grp=grp)
            for member in Member_SET:
                print 'test3'
                usr = member.member
                call = usr.phonenumber
                event = Event.objects.get(id = eid)
                time = str(event.datetime)
                info = event.name + time
                message = {'username': 'Amar', 'api_password':'4de4cegbv5sjcaj3e', 'sender':'test', 'to':call,'message':info, 'priority':2}
                parameter = urllib.urlencode(message)
                req = urllib2.Request(url='http://bulksms.gateway4sms.com/pushsms.php?',data = parameter)
                f = urllib2.urlopen(req)
                print f.read()
            group_event.delete()
            if row.event.pre_prep == None:
                row.event.delete()
            else:
                row.event.pre_prep.delete()
                row.event.delete()
            msg = 'Delete successful!'
            msg_type = 'success'
            return render_to_response("notify/notify.html", {'msg': msg, 'msg_type': msg_type})
    msg = 'Delete unsuccessful!'
    msg_type = 'warning'
    return render_to_response("notify/success.html", {'msg': msg, 'msg_type': msg_type})

@login_required(login_url = '/login/')
def show_events(request, gid):
    grp = group.objects.get(id = gid)
    members = groupmem.objects.filter(grp = grp)
    member = students.objects.get(studentid = request.user.username)
    if grp.groupadmin == int(request.user.username):
        admin = True
    else:
        admin = False
    for each in members:
        if member == each.member:
            events = groupevent.objects.filter(grp = grp)
            if events:
                no_events = False
            else:
                no_events = True
            print no_events
            group_events = []
            if no_events == False:
                for e in events:
                    print e.event
                    row = Event.objects.get(id = e.event)
                    group_events.append(row)
                    #for table in (Lecture, Club, Project, Exam, Sport, Other):
                    #    row = table.objects.get(id = e.event)
                    #    if row:
                    #        group_events.append(row)
            return render_to_response('groups/group_events.html', {'gid': gid, 'group_events': group_events, 'admin': admin, 'no_events': no_events})
    msg = "You are not permitted to view this page"
    msg_type = "warning"
    return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})                    

@login_required(login_url = '/login/')
def create_topic(request, gid):
    grp = group.objects.get(id = gid)
    members = groupmem.objects.filter(grp = grp)
    member = students.objects.get(studentid = request.user.username)
    for each in members:
        if member == each.member:
            if request.method == 'POST':
                new_topic = Thread(title = request.POST['title'], created = datetime.datetime.now(), creator = request.user, forum = grp.forum)
                new_topic.save()
                url = '/forum/' + str(grp.forum.pk) + '/'
                return HttpResponseRedirect(url)
            else:
                return render_to_response('forum/create_thread.html', {'gid': gid, 'forum': grp.forum}, context_instance=RequestContext(request))
    msg = "You are not permitted to create a topic for this group"
    msg_type = 'warning'
    return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})

    
