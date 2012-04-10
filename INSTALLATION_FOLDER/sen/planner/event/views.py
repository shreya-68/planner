# Create your views here.
#

from django.forms.models import modelformset_factory
from django.contrib.auth.decorators import login_required 
from django.core.context_processors import csrf  
from django.http import HttpResponse, Http404
from django.core.urlresolvers import reverse
from event.forms import *
from event.models import *
from django.template import RequestContext, loader
from django.shortcuts import render_to_response, get_object_or_404
from usrper import *
from schedule.models import *
import datetime
#define id of student on login, var = stid, determine way of getting it

def notify(request):
    msg = "Message delivered"
    msg_type = "success"
    render_to_response('notify/notify.html', msg = msg, msg_type = msg_type)

@login_required(login_url = '/login/')
def all_events(request):
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
#    if event_type_id == '1':
#        events_list = Lecture.objects.all()
#    elif event_type_id == '2':
#        events_list = Project.objects.all()
#    elif event_type_id == '4':
#        events_list = Club.objects.all()
#    elif event_type_id == '5':
#        events_list = Other.objects.all()
#    else:
#        raise Http404
    return render_to_response('event/event_type_detail.html', {'events_list': events_list})
    

@login_required(login_url = '/login/')
def view_event_detail(request, event_type_id, event_id):      
#    event_type = Event_Type.objects.get(id = event_type_id)
#    event_type = event_type.get_event_type_display
#    event_detail = event_type.objects.get(id = event_id)
    for row in Event_Type.objects.all():
        if row.id == int(event_type_id):
        	event_name = row.get_event_type_display()
        	event_detail = globals()[event_name].objects.get(id = event_id)
        	if event_detail.event.user != request.user:
        		return HttpResponse("User not allowed to access this page")
#    if event_type_id == '1':
#        event_detail = Lecture.objects.get(id=event_id)
#    elif event_type_id == '2':
#        event_detail = Project.objects.get(id=event_id)
#    elif event_type_id == '4':
#        event_detail = Club.objects.get(id=event_id)
#    elif event_type_id == '5':
#        event_detail = Other.objects.get(id=event_id)
#    else:
#        raise Http404
   #this_event = {{event_type.get_event_display}}.objects.get(id=event_id)
    return render_to_response('event/event_detail.html', {'event_detail': event_detail })

#def enter_date(request):

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
        return render_to_response("event/create-event.htm", {'form':form, 'eventform': eventform, 'courses': courses, 'event_type': event_type
	                    }, context_instance=RequestContext(request))
    




@login_required(login_url = '/login/')
def edit_event(request, eid):
    """Edit this event"""
    if request.method == 'POST':
        for table in (Lecture, Club, Project, Exam, Sport, Other):
    	    row = table.objects.get(id = eid)
            if row:
            	form = EventForm(request.POST, instance = row)
                if form.is_valid():
                	form.save()
                	msg = 'Event edited successfully!'
                	return render_to_response("notify/success.html", msg = msg)
    else:
        for table in (Lecture, Club, Project, Exam, Sport, Other):
    	    row = table.objects.get(id = eid)
            if row.event.user == request.user:
            	return render_to_response("event/edit_event.html", event = row)
            else:
                return HttpResponse("Cannot access this page")

            	
                
    	             

@login_required(login_url = '/login/')
def delete_event(request, eid):
    """Delete an event with pk"""

    for table in (Lecture, Club, Project, Exam, Sport, Other):
    	row = table.objects.get(id = eid)
        if row.event.user == request.user:
        	row.delete()
        	msg = 'Delete successful!'
        	return render_to_reponse("notify/success.html", msg = msg)
    msg = 'Delete unsuccessful!'
    return render_to_reponse("notify/success.html", msg = msg)

    


        


def add_csrf(request, **kwargs):
    """Add CSRF and user to dictionary"""
    d=dict(user=request.user, **kwargs)
    d.update(csrf(request))
    return d


def plan(request):
    return render_to_response('plan/plan.html')

def plan_date(request):
    return render_to_response('plan/input_date.html')

@login_required(login_url = '/login/')
#def create_plan(request,year,month,day):
def create_plan(request):

    year = request.POST['year']
    month = request.POST['month']
    day = request.POST['day']

    fixedEvents = []

    for table in (Lecture, Club, Project, Exam, Sport, Other):
    	date = datetime.date(int(year), int(month), int(day))
    	tableEvents = table.objects.filter(event__datetime__range = (datetime.datetime.combine(date, datetime.time.min), datetime.datetime.combine(date, datetime.time.max)))
    	tableEvents = tableEvents.order_by('event__datetime')

        for row in tableEvents:
        	#It is a fixed event so start_time will be the time of the event occuring on this day.
            row.event.start_time = row.event.datetime
#            print row.event.start_time
#duration is a time field so hour and minute is extracted and converted into timedelta
            duration_hours = row.event.duration.hour
            duration_minutes = row.event.duration.minute
            duration = datetime.timedelta(hours=duration_hours,minutes= duration_minutes) #   duration = row.event.duration - datetime.datetime.combine(row.event.duration.date(), datetime.time.min)
#            print duration
			#end_time of a fixed event occuring today is start_time + duration of event 
            row.event.end_time = row.event.datetime + duration #row.event.quantum_time = datetime.datetime.combine(date, row.event.duration.time())
#            print row.event.end_time
       #     row.event.quantum_time = duration
#            print row.event.quantum_time
            fixedEvents.append(row)
           # print len(fixedEvents)

#    from django.db import connection
#    from pprint import pprint
#    pprint( connection.queries)
    
    pre_prepEvents = []

    for table in (Lecture, Club, Project, Exam, Sport, Other):
    	tableEvents = table.objects.filter(event__pp = True)
# compute event__priority = 
#    	tableEvents = tableEvents.order_by('event__priority')

        for row in tableEvents:
            row.event.start_time = datetime.datetime.combine(date, datetime.time.min)
            timeleft = row.event.datetime - row.event.start_time
            workleft = row.event.pre_prep.duration - row.event.pre_prep.complete
        	#row.event.priority = row.event.Type.priority*0.4 + row.user_difficulty*0.4 + timeleft 
#            duration_hours = workleft.hours
#            duration_minutes = workleft.minutes 
#            duration = datetime.timedelta(hours=duration_hours,minutes= duration_minutes)
#            print duration
            row.event.end_time = row.event.datetime + workleft 

            if ( row.event.pre_prep.quantum_time == None):
            	row.event.pre_prep.quantum_time = workleft
            	#row.event.quantum_time = datetime.datetime.combine(date, row.event.duration.time())
            else:
            	row.event.pre_prep.quantum_time = row.event.pre_prep.quantum_time - datetime.datetime.combine(row.event.pre_prep.quantum_time.date(), datetime.time.min)
            	#row.event.pre_prep.quantum_time = datetime.datetime.combine(date, row.event.duration.time())
            row.event.pre_prep.max_eff = datetime.datetime.combine(date, row.event.pre_prep.max_eff.time())
            pre_prepEvents.append(row)
        pre_prepEvents = sorted(pre_prepEvents, key=lambda table: table.event.priority)
   # print len(fixedEvents)
   # test = fixedEvents
   # for row in pre_prepEvents:
   #     if (row not in fixedEvents):
   # 	    test.append(row)
    
   # print len(fixedEvents)
   # for x in fixedEvents:
   # 	print x.event.name
   # print len(pre_prepEvents)
   # for x in pre_prepEvents:
   # 	print x.event.name
    #return render_to_response('event/event_type_detail.html', {'events_list': test})
    return schedule(fixedEvents, pre_prepEvents, date)

def schedule(fixedEvents, pre_prepEvents, date):

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

    #time1 = (event_detail.event.start_time.hour*12) + (event_detail.event.start_time.minute/5)
    #return render_to_response('plan/slider.html', {'event_detail': event_detail, 'time1': time1 })
    return render_to_response('event/event_type_detail.html', {'events_list': fixedEvents})

def test(request):
    counter = 3
    return render_to_response('plan/time-line.htm', {'ctr': range(counter)})
