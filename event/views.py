# Create your views here.
#

from django.http import HttpResponse, Http404
from event.models import *
from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404


def all_events(request):
    event_types = Event_Type.objects.all()
    return render_to_response('events/all_events.html', {'event_types': event_types})

    
def event_type_detail(request, event_type_id):
    event_type = Event_Type.objects.get(id=event_type_id)
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
    return render_to_response('events/event_type_detail.html', {'events_list': events_list})
    

def event_detail(request, event_type_id, event_id):      
    #event_type = Event_Type.objects.get(id=event_type_id)
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
    return render_to_response('events/event_detail.html', {'event_detail': event_detail })

def create_plan(request)
    l = Lecture.objects.filter(ltiming__year == 2012 && ltiming__month == 2 && ltiming__day == 29)
    l = l.order_by(ltiming)
    c = Club.objects.filter(e_time__date == datetime.now())
    o = Other.objects.filter(time__date == datetime.now())
    arr[]
    for i in range(0,47):
    	arr = arr.append(None)
    for i in range(0,l.len()-1)
    	x = (l[i].ltiming__hour*2)+(int)(l[i].ltiming__minute/30)
    	arr[x]=l[i]

    for i in range(0,c.len()-1)
    	x = (c[i].e_time__hour*2)+(int)(c[i].e_time__minute/30)
    	arr[x]=c[i]
        
    for i in range(0,l.len()-1)
    	x = (o[i].time__hour*2)+(int)(o[i].time__minute/30)
    	arr[x]=o[i]








