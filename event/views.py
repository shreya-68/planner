# Create your views here.
#

from django.forms.models import modelformset_factory
from django.contrib.auth.decorators import login_required 
from django.core.context_processors import csrf  
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from event.forms import *
from event.models import *
from usrper.models import *
from groups.models import *
from django.template import RequestContext, loader
from django.shortcuts import render_to_response, get_object_or_404
from usrper import *
from schedule.models import *
import datetime
import urllib
import urllib2
#define id of student on login, var = stid, determine way of getting it

def notify(request):
    msg = "Message delivered"
    msg_type = "success"
    render_to_response('notify/notify.html', msg = msg, msg_type = msg_type)

@login_required(login_url = '/login/')
def all_events(request):
    events = Event.objects.all()
    for each in events:
        print each.id
    event_types = Event_Type.objects.all()
    return render_to_response('event/all_events.html', {'event_types': event_types})

    
@login_required(login_url = '/login/')
def event_type_detail(request, event_type_id):
    #event_type = Event_Type.objects.get(id=event_type_id)
    #event_name = event_type.get_event_display
    #return render_to_response('events/test.html', {'event_type_id': event_type_id})
    print event_type_id
    events_list = []
    for row in Event_Type.objects.all():
        if row.id == int(event_type_id):
            event_name = row.get_event_type_display()
            events_list = globals()[event_name].objects.filter(event__user = request.user)
    return render_to_response('event/event_type_detail.html', {'events_list': events_list})
    

@login_required(login_url = '/login/')
def view_event_detail(request, event_type_id, event_id):      
    for row in Event_Type.objects.all():
        if row.id == int(event_type_id):
            event_name = row.get_event_type_display()
            event_detail = globals()[event_name].objects.get(id = event_id)
            if event_detail.event.user != request.user:
                return HttpResponse("User not allowed to access this page")
    return render_to_response('event/event_detail.html', {'event_detail': event_detail })


@login_required(login_url = '/login/')
def add_event(request):
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
                new_event = eventform.save(commit = False)
                print new_event.datetime
                print new_event.datetime > datetime.datetime.now()
                if new_event.datetime > datetime.datetime.now():
                    print request.user
                    print new_event.pp
                    new_event.user = request.user 
                    #eventform.start_time = '2/3/2012 00:00:00'
                    #eventform.end_time = '2/3/2012 21:00:00'
                    if request.POST['pp'] == True:
                        new_event.pre_prep = pre_prep
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
                    return HttpResponseRedirect('/calendar/month/')      
                else:
                    return HttpResponse('Event has to occur after today\'s date.')
            else:
                return render_to_response('notify/errorlist.html', {'eventform': eventform})
        else:
            return render_to_response('notify/errorlist.html', {'form': form})
    else:
        date = datetime.date.today()
        day = date.day
        month = date.month
        year = date.year
        date = str(month)+'/'+str(day)+'/'+str(year)
        form = PrePrepForm()
        event_type = Event_Type.objects.all()
        usr = students.objects.get(studentid = int(request.user.username))
        courses = UserCourses.objects.filter(user = usr)
        eventform = EventForm(instance = Pre_prep())
        return render_to_response("event/add_event.html", {'form':form, 'eventform': eventform, 'courses': courses, 'event_type': event_type, 'date': date
                        }, context_instance=RequestContext(request))
    




@login_required(login_url = '/login/')
def edit_event(request, eid):
    """Edit this event"""
    if request.method == 'POST':
        row = Event.objects.get(id = eid)
        if row.exists():
            form = EventForm(request.POST, instance = row)
            if form.is_valid():
                event = form.save(commit = False)
                if event.datetime > datetime.datetime.now():
                    form.save()
                    return HttpResponseRedirect('/calendar/month/')      
            else:
                url = '/edit_event/' + str(eid) + '/'
                return HttpResponseRedirect(url)
    else:
        for table in (Lecture, Club, Project, Exam, Sport, Other):
            row = table.objects.get(id = eid)
            if row.event.user == request.user:
                date = row.event.datetime.date()
                time = row.event.datetime.time()
                duration = row.event.duration.time()
                return render_to_response("event/edit_event.html", {'event': row, 'date': date, 'time': time, 'duration': duration}, context_instance = RequestContext(request))
            else:
                return HttpResponse("Invalid User, cannot access this page")
    msg = "This event does not exist"
    msg_type = 'warning'
    return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})

                
                
                     

@login_required(login_url = '/login/')
def delete_event(request, eid):
    """Delete an event with pk"""

    for table in (Lecture, Club, Project, Exam, Sport, Other):
        row = table.objects.get(id = eid)
        if row.event.user == request.user:
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
    return render_to_reponse("notify/success.html", {'msg': msg, 'msg_type': msg_type})

    

def add_csrf(request, **kwargs):
    """Add CSRF and user to dictionary"""
    d=dict(user=request.user, **kwargs)
    d.update(csrf(request))
    return d


def plan(request):
    return render_to_response('plan/input_date.html', context_instance = RequestContext(request))

def add_lecture_event(request, date):
    day = date.weekday()
    print day
    user = students.objects.get(studentid = int(request.user.username))
    course_list = UserCourses.objects.filter(user = user)
    for course in course_list:
    	print course.course.id
        days = CourseLecture.objects.filter(course = course.course)
        for each_day in days:
            if each_day.day == day:
                print date
                print datetime.datetime.combine(date, each_day.time.time())
                lecture_event = Event(name = course.course.name, datetime = datetime.datetime.combine(date, each_day.time.time()), duration = datetime.datetime.combine(date, each_day.duration.time()), pp = False, priority = 1, remind = False, user = request.user, user_difficulty = 1)
                lecture_event.save()
                event_type = Event_Type.objects.get(id = 1)
                new_event = Lecture(course = course.course, Type = event_type, event = lecture_event) 
                new_event.save()
    return 1


@login_required(login_url = '/login/')
def create_plan(request):
    try:
        date = request.POST['date']
        date = date.split('/')
        day = int(date[0])
        month = int(date[1])
        year = int(date[2])
        print day, month, year
    except:
        return HttpResponseRedirect('/plan/')

    date = datetime.date(int(year), int(month), int(day))
    if date < datetime.date.today():
    	return HttpResponseRedirect('/plan/')

    fixedEvents = []

    for table in (Lecture, Club, Project, Exam, Sport, Other):
        tableEvents = table.objects.filter(event__user = request.user).filter(event__datetime__range = (datetime.datetime.combine(date, datetime.time.min), datetime.datetime.combine(date, datetime.time.max)))
        tableEvents = tableEvents.order_by('event__datetime')

        for row in tableEvents:
            #It is a fixed event so start_time will be the time of the event occuring on this day.
            row.event.start_time = row.event.datetime
#            print row.event.start_time
#duration is a time field so hour and minute is extracted and converted into timedelta
            duration_hours = row.event.duration.hour
            duration_minutes = row.event.duration.minute
            duration = datetime.timedelta(hours=duration_hours,minutes= duration_minutes) 
            #end_time of a fixed event occuring today is start_time + duration of event 
            row.event.end_time = row.event.datetime + duration #row.event.quantum_time = datetime.datetime.combine(date, row.event.duration.time())
#            print row.event.end_time
            fixedEvents.append(row)

    pre_prepEvents = []

    for table in (Lecture, Club, Project, Exam, Sport, Other):
        tableEvents = table.objects.filter(event__user = request.user).filter(event__pp = True).filter(event__datetime__gt = datetime.datetime.combine(date, datetime.time.min))
        
        if tableEvents:
            for row in tableEvents:
                print row
                print row.event.name
                print row.event.pp
                if row.event.pre_prep != None:
                    row.event.start_time = datetime.datetime.combine(date, datetime.time.min)
                    row.event.pre_prep.duration = datetime.datetime.combine(date, row.event.pre_prep.duration.time())
                    row.event.pre_prep.complete = datetime.datetime.combine(date, row.event.pre_prep.complete.time())
                    timeleft = row.event.datetime - row.event.start_time
                    workleft = row.event.pre_prep.duration - row.event.pre_prep.complete
                    #row.event.priority = row.event.Type.priority*0.4 + row.user_difficulty*0.4 + timeleft 
                    row.event.end_time = row.event.datetime + workleft 

                    if ( row.event.pre_prep.quantum_time == None):
                        row.event.pre_prep.quantum_time = workleft
                    else:
                        row.event.pre_prep.quantum_time = row.event.pre_prep.quantum_time - datetime.datetime.combine(row.event.pre_prep.quantum_time.date(), datetime.time.min)
                        #row.event.pre_prep.quantum_time = datetime.datetime.combine(date, row.event.duration.time())
                    row.event.pre_prep.max_eff = datetime.datetime.combine(date, row.event.pre_prep.max_eff.time())
                    pre_prepEvents.append(row)
            pre_prepEvents = sorted(pre_prepEvents, key=lambda table: table.event.priority)
    return schedule(request, fixedEvents, pre_prepEvents, date)

def schedule(request, fixedEvents, pre_prepEvents, date):

    print request.user.username
    for pre_prep_event in pre_prepEvents:
        min_time = datetime.time.min 
        insert_here = -1
        mark = -1
        free = 0
        j = 0
        for j in range(len(fixedEvents)-1):
            #if (fixedEvents[j].event.start_time == None):
            #    fixedEvents[j].event.start_time = fixedEvents[j].event.datetime
            if(pre_prep_event.event.pre_prep.max_eff < fixedEvents[j].event.start_time and pre_prep_event.event.pre_prep.max_eff > fixedEvents[j].event.end_time ):
                free = 1
                break;

        if fixedEvents[j].event.pre_prep.quantum_time == None:
            fixedEvents[j].event.pre_prep.quantum_time = datetime.datetime.combine(date, datetime.time(0,30,0))
# start time - quantum time > 
        #fixedEvents[j].event.start_time - fixedEvents[j].event.pre_prep.quantum_time > pre_prep_event.event.pre_prep.max_eff - datetime.datetime.combine(pre_prep_event.event.pre_prep.max_eff.date(),datetime.time.min)):
        if(free ==1 and fixedEvents[j].event.start_time - pre_prep_event.event.pre_prep.max_eff > pre_prep_event.event.pre_prep.quantum_time):
            pre_prep_event.event.start_time = pre_prep_event.event.pre_prep.max_eff
            pre_prep_event.event.end_time = pre_prep_event.event.start_time + pre_prep_event.event.pre_prep.quantum_time 
            pre_prep_event.event.pre_prep.complete = pre_prep_event.event.pre_prep.complete - pre_prep_event.event.pre_prep.quantum_time 
        elif ( free == 1 and fixedEvents[j].event.start_time - fixedEvents[j-1].event.end_time > pre_prep_event.event.pre_prep.quantum_time):
            pre_prep_event.event.start_time = fixedEvents[j].event.start_time - pre_prep_event.event.pre_prep.quantum_time
            pre_prep_event.event.end_time = fixedEvents[j].event.start_time
            pre_prep_event.event.pre_prep.complete = pre_prep_event.event.pre_prep.complete - pre_prep_event.event.pre_prep.quantum_time
            insert_here = j-1
        else:
            i = j
            for i in range(j,len(fixedEvents)-1):
                fixed_event = fixedEvents[i]
                next_event = fixedEvents[i+1]
                time_gap = next_event.event.start_time - fixed_event.event.end_time
                time_slice =  pre_prep_event.event.pre_prep.quantum_time
                if (min_time == datetime.time.min or time_gap < min_time) and time_gap >= time_slice:
                    min_time = time_gap
                    insert_here = i+1
        if (insert_here != -1):
            fixedEvents.insert(insert_here, pre_prep_event)

    lst = []
    for each_event in fixedEvents:
        hour = int(each_event.event.start_time.hour)
        minute = int(each_event.event.start_time.minute)
        margin_left = (hour*147) + (minute*147/60)
        print margin_left
        print each_event.event.end_time
        duration = each_event.event.end_time - each_event.event.start_time
        hour = duration.seconds/3600
        print hour
        minute = (duration.seconds%3600)/60
        print minute
        width = (hour*147) + (minute*147/60)
        print width
        lst.append((each_event, margin_left, width)) 

    other_events = []
    user = students.objects.get(studentid = int(request.user.username))
    if user.sleephours == None:
        return render_to_response('plan/planner.html', {'lst': lst, 'date':date}, context_instance=RequestContext(request))

    name = "Sleep time"
    time = user.sleephours.time()
    hour = int(user.sleephours.hour)
    minute = int(user.sleephours.minute)
    margin_left = (hour*150) + (minute*150/60)
    width = (user.wakeup.hour*150) + (user.wakeup.minute*150/60)
    other_events.append((name, time, margin_left, width))
    if user.lunchtime == None:
        return render_to_response('plan/planner.html', {'lst': lst, 'other_events': other_events, 'date':date}, context_instance=RequestContext(request))
    name = "Lunch time"
    time = user.lunchtime.time()
    hour = int(user.lunchtime.hour)
    minute = int(user.lunchtime.minute)
    margin_left = (hour*150) + (minute*150/60)
    width = 75 
    other_events.append((name, time, margin_left, width))
    if user.dinnertime == None:
        return render_to_response('plan/planner.html', {'lst': lst, 'other_events': other_events, 'date':date}, context_instance=RequestContext(request))
    name = "Dinner time"
    time = user.dinnertime.time()
    hour = int(user.dinnertime.hour)
    minute = int(user.dinnertime.minute)
    margin_left = (hour*150) + (minute*150/60)
    width = 75 
    other_events.append((name, time, margin_left, width))

    return render_to_response('plan/planner.html', {'lst': lst, 'other_events': other_events, 'date':date}, context_instance=RequestContext(request))

def test(request):
    counter = 3
    return render_to_response('plan/time-line.htm', {'ctr': range(counter)})

