# Create your views here.
import time
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.core.context_processors import csrf
from django.forms.models import modelformset_factory
from django.shortcuts import get_object_or_404, render_to_response
from event.models import *
from usrper.models import *
from event.views import *
from schedule.models import *
from datetime import date, datetime, timedelta
import calendar

month_names = "January February March April May June July August September October November December"
month_names = month_names.split()

@login_required(login_url = '/login/')
def view_year(request, year = None):
    """
    """
#prev / next years
    if year: year = int(year)
    else: year = time.localtime()[0]

    now_year, now_month = time.localtime()[:2]
    lst = []

# create a list of months for each year, indicating ones that contain entries and current
    for y in [year, year+1, year +2]:
        mlst = []
        for n, month in enumerate(month_names):
            entry = current = False # are there entries for the current month?
            
            entries = Event.objects.filter(datetime__year = y, datetime__month = n+1, user__username = request.user.name)
            if entries:
                entry = True
            if y == now_year and n+1 == now_month:
                current = True
            mlst.append(dict(n=n+1, name=month, entry=entry, current=current))
        lst.append((y, mlst))

    return render_to_response("cal/main.html", dict(years = lst, user = request.user, year = year, reminders = reminders(request)))

@login_required(login_url = '/login/')
def view_month(request, year = None , month = None, change = None):
    """
    Listing of days in month
    """

    if (year == None and month == None):
        year, month = time.localtime()[:2]

    year, month = int(year), int(month)

#apply next/ previous change
    if change in ("next","prev"):
        now, mdelta = date(year, month, 15), timedelta(days = 30)
        if change == "next":
            year, month = (now + mdelta).timetuple()[:2]
        elif change == "prev": year, month = (now - mdelta).timetuple()[:2]

    #init variables
    cal = calendar.Calendar()
    month_days = cal.itermonthdays(year, month)
    now_year, now_month, now_day = time.localtime()[:3]
    lst = [[]]
    week = 0

# make month lists contain list of days for each week
    # each day tuple will contain list of entries and current indicator
    for day in month_days:
        entries = current = False
        number = 0
        if day:
            this_date = date(int(year), int(month), int(day))
            entries = Event.objects.filter(user = request.user, datetime__year = year, datetime__month = month, datetime__day = day)
            number = len(entries)
            if day == now_day and year == now_year and month == now_month:
                current = True

        lst[week].append((day, entries, current, number))
        if len(lst[week]) == 7:
            lst.append([])
            week += 1

    return render_to_response("cal/view_month.html", dict(year = year, month = month, user = request.user, month_days = lst, month_name = month_names[month-1], reminders = reminders(request)), context_instance = RequestContext(request))

@login_required(login_url = '/login/')
def add_event_to_date(request, year, month, day):
    """ Entries for the day"""
    EntriesFormset = modelformset_factory(Event, extra= 1, exclude = ("user"), can_delete = True)
    if request.method == 'POST':
        formset = EntriesFormset(request.POST)
        if formset.is_valid():
# add current user to each entry and save
            entries = formset.save(commit = False)
            for entry in entries:
                entry.creator = request.user
                #entry.date = date(int(year), int(month), int(day))
                entry.save()
            return HttpResponseRedirect(reverse("schedule.views.view_month", args=(year,month)))
    else:
#display formset
        formset = EntriesFormset(queryset=Event.objects.filter(datetime__year=year,datetime__month=month, datetime__day=day, user=request.user))
    return render_to_response("cal/add_event.html", add_csrf(request, entries=formset, year=year, month=month, day=day))



@login_required(login_url = '/login/')
def add_csrf(request, **kwargs):
    """Add CSRF and user to dictionary"""
    d=dict(user=request.user, **kwargs)
    d.update(csrf(request))
    return d

@login_required(login_url = '/login/')
def view_day(request, year = None, month = None, day = None, change = None):
    """ View entries in a day"""

    if (year == None and month == None and day == None):
        year, month, day = time.localtime()[:3]
    year, month, day = int(year), int(month), int(day)

#apply next/ previous change
    if change in ("next","prev"):
        now, mdelta = date(year, month, day), timedelta(days = 7)
        if change == "next":
            year, month, day = (now + mdelta).timetuple()[:3]
        elif change == "prev": year, month, day = (now - mdelta).timetuple()[:3]


#init variables
    cal = calendar.Calendar(0)
    now_year, now_month, now_day = time.localtime()[:3]
    weeks = cal.monthdayscalendar(year, month)
    lst = []

#make week list contain list of days for that week
#get week tuple for current week

    for week in weeks:
        if day in week:
            for days in week:
                entries= current = False
                if days:
                    entries = Event.objects.filter(datetime__year=year,datetime__month=month, datetime__day=days, user=request.user)
                    if days == day:
                        current = True
                lst.append((days, entries, current))
            break;
# each week tuple will contain list of entries and current indicator
    return render_to_response("cal/view_day.html", add_csrf(request, year=year, month=month, day=day, week_days = lst, month_name = month_names[month-1]))

def reminders(request):
    """ Return the list of reminders for today and tomorrow"""
    year, month, day = time.localtime()[:3]
    reminders = Event.objects.filter(datetime__year = year, datetime__month = month, datetime__day = day, user = request.user, remind=True)
    tomorrow = datetime.now() + timedelta(days= 1)
    year, month, day = tomorrow.timetuple()[:3]
    return list(reminders) + list(Event.objects.filter(datetime__year=year, datetime__month=month, datetime__day = day, user = request.user, remind=True))

def _show_users(request):
    """
    """
    s = request.session
    if not "show_users" in s:
        s["show_users"] =True
    return s["show_users"]

def settings(request):
    """
    Settings screen
    """

    s= request.session
    _show_users(request)
    if request.method == "POST":
        s["show_users"] = (True if "show_users" in request.POST else False)
    return render_to_response("cal/settings.html", add_csrf(request, show_users = s["show_users"]))


