# Create your views here.
#

from django.http import HttpResponse, Http404
from event.models import *
from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from usrper import *
from schedule.models import *
import datetime
#define id of student on login, var = stid, determine way of getting it

def all_events(request):
    event_types = Event_Type.objects.all()
    return render_to_response('event/all_events.html', {'event_types': event_types})

    
def event_type_detail(request, event_type_id):
    #event_type = Event_Type.objects.get(id=event_type_id)
    #event_name = event_type.get_event_display
    #return render_to_response('events/test.html', {'event_type_id': event_type_id})
    if event_type_id == '1':
        events_list = Lecture.objects.all()
    elif event_type_id == '2':
        events_list = Project.objects.all()
    elif event_type_id == '4':
        events_list = Club.objects.all()
    elif event_type_id == '5':
        events_list = Other.objects.all()
    else:
        raise Http404
    return render_to_response('event/event_type_detail.html', {'events_list': events_list})
    

def event_detail(request, event_type_id, event_id):      
#    event_type = Event_Type.objects.get(id = event_type_id)
#    event_type = event_type.get_event_type_display
#    event_detail = event_type.objects.get(id = event_id)
    if event_type_id == '1':
        event_detail = Lecture.objects.get(id=event_id)
    elif event_type_id == '2':
        event_detail = Project.objects.get(id=event_id)
    elif event_type_id == '4':
        event_detail = Club.objects.get(id=event_id)
    elif event_type_id == '5':
        event_detail = Other.objects.get(id=event_id)
    else:
        raise Http404
   #this_event = {{event_type.get_event_display}}.objects.get(id=event_id)
    return render_to_response('event/event_detail.html', {'event_detail': event_detail })

#def enter_date(request):
    
def create_plan(request,year,month,day):

    fixedEvents = []
#    LectureEvents = Lecture.objects.filter(event__datetime__date= datetime.date(y,m,d))
  #   LectureEvents = LectureEvents.order_by(event__time)
#    ClubEvents = Club.objects.filter(event__datetime.date() = datetime.date(y,m,d))
#    ClubEvents = ClubEvents.order_by(event__time)
#    ProjectEvents = Project.objects.filter(event__datetime.date() = datetime.date(y,m,d))
#    ProjectEvents = ProjectEvents.order_by(event__time)
#    ExamEvents = Exam.objects.filter(event__datetime.date() = datetime.date(y,m,d))
#    SportEvents = Sport.objects.filter(event__datetime.date() = datetime.date(y,m,d))
#    OtherEvents = Other.objects.filter(event__datetime.date() = datetime.date(y,m,d))
#    test = []    
#    date = datetime.date(int(year), int(month), int(day))
#    tableEvents = Lecture.objects.filter(event__datetime__range = (datetime.datetime.combine(date, datetime.time.min), datetime.datetime.combine(date, datetime.time.max)))
#    for row in tableEvents:
#    	test.append(row)
    for table in (Lecture, Club, Project, Exam, Sport, Other):
    	date = datetime.date(int(year), int(month), int(day))
    	tableEvents = table.objects.filter(event__datetime__range = (datetime.datetime.combine(date, datetime.time.min), datetime.datetime.combine(date, datetime.time.max)))
    	tableEvents = tableEvents.order_by('event__datetime')
        for row in tableEvents:
        	 fixedEvents.append(row)
    from django.db import connection
    from pprint import pprint
    pprint( connection.queries)
#    for table in (LectureEvents):
#       fixedEvents.append(table)
#    for table in ( ProjectEvents):
#       fixedEvents.append(table)
#    for table in ( ClubEvents):
#       fixedEvents.append(table)
#    for table in (ExamEvents):
#       fixedEvents.append(table)
#    for table in (SportEvents):
#       fixedEvents.append(table)
#    for table in (OtherEvents):
#       fixedEvents.append(table)
    pre_prepEvents = []
#    LectureEvents = Lecture.objects.filter()
#    ClubEvents = Club.objects.filter(event__pre_prep = True)
#    ProjectEvents = Project.objects.filter(event__pre_prep = True)
#    ExamEvents = Exam.objects.filter(event__pre_prep = True)
#    SportEvents = Sport.objects.filter(event__pre_prep = True)
#    OtherEvents = Other.objects.filter(event__pre_prep = True)
    for table in (Lecture, Club, Project, Exam, Sport, Other):
    	tableEvents = table.objects.filter(event__pre_prep = True)
    	tableEvents = tableEvents.order_by('event__datetime')
        for row in tableEvents:
        	pre_prepEvents.append(row)
#    for table in (LectureEvents):
#       pre_prepEvents.append(table)
#    for table in ( ProjectEvents):
#       pre_prepEvents.append(table)
#    for table in ( ClubEvents):
#       pre_prepEvents.append(table)
#    for table in (ExamEvents):
#       pre_prepEvents.append(table)
#    for table in (SportEvents):
#       pre_prepEvents.append(table)
#    for table in (OtherEvents):
#       pre_prepEvents.append(table)
    test = fixedEvents
    for row in pre_prepEvents:
        if (row not in fixedEvents):
    	    test.append(row)
    return render_to_response('event/event_type_detail.html', {'events_list': test})
 #   schedule(fixedEvents, pre_prepEvents)
#
#def schedule(fixedEvents, pre_prepEvents):

#    fixedEvents = list(events.filter(event__datetime.date() = datetime.date(y,m,d)).order_by(event__time))
#    pre_prepEvents = list(events.filter(event.pre_prep = True).order_by(event.priority))
#    hobby = 
######    for pre_prep_event in pre_prepEvents:
######        min_time = -1 
######        insert_here = -1
######        for i in range(len(fixedEvents)-1):
######            fixed_event = fixedEvents[i]
######            next_event = fixedEvents[i+1]
######            time_gap = next_event.event.datetime - fixed_event.event.datetime # + fixed_event.event.duration
#    return render_to_response('event/event_detail.html', {'event_detail': pre_prep_event })
###            if (min_time == -1 or time_gap < min_time) and time_gap>= (pre_prep_event.event.datetime.time():
####            	eff = find_efficiency(fixed_event.event__time + fixed_event.event__duration) 
####            	if ( eff in range(pre_prep_event.event.priority + 2, pre_prep_event.event__time - 2))
###                min_time = time_gap
###            	insert_here = i 
###        fixedEvents.insert(insert_here+1, pre_prep_event)
###    return render_to_response('event/event_type_detail.html', {'events_list': fixedEvents})
#
#def find_efficiency(time)
#    max_eff = Student.objects.get(id=user_id).max_eff
#    eff = abs(max_eff-time)
#    eff = math.floor(eff)
#    return eff
#
#


#    for fixed_event in fixedevents:
#    	eff = find_efficiency(fixed_event.event.start_time + fixed_event.event.end_time)
#       	time_gap = next_event.event__time - fixed_event.event__time + fixed_event.event.duration
#        while (time_gap>0):
#            for pre_prep_event in pre_prepEvents:
#                if ( (eff in range(pre_prep_event.event.priority + 2, pre_prep_event.event__time - 2)) and time_gap> pre_prep_event.event.block_time and time_gap < min_time):
#                	min_time = time_gap
#                    i = pre_prepEvents.index(pre_prep_event
#















    
##    c = Club.objects.filter(e_time__date == datetime.now())
##    o = Other.objects.filter(time__date == datetime.now())

##    for i in range(0,47):
##    	arr = arr.append(None)
##    
##    for i in range(0,l.len()-1)
##    	x = (l[i].ltiming__hour*2)+(int)(l[i].ltiming__minute/30)
##    	arr[x]=l[i]
##
##    for i in range(0,c.len()-1)
##    	x = (c[i].e_time__hour*2)+(int)(c[i].e_time__minute/30)
##    	arr[x]=c[i]
##        
##    for i in range(0,o.len()-1)
##    	x = (o[i].time__hour*2)+(int)(o[i].time__minute/30)
##    	arr[x]=o[i]
##    student_info = students.objects.get(studentid=stid)
##    x = (student_info.sleephours__hour*2)+ (int)student_info.sleephours__minute/30)
##    y = (student_info.waketime__hours*2) + (int)student_info.waketime__minute/30)
##    for i in range(x,y)
##    	arr[i]="sleep"
##     
##    x = (student_info.lunchtime__hour*2)+ (int)student_info.lunchtime__minute/30)
##    arr[x]="lunch"
##    x = (student_info.dinnertime__hour*2)+ (int)student_info.dinnertime__minute/30)
##    arr[x]="dinner"
##    for i in range(0,47)
##    	x 



