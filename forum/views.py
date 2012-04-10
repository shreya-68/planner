# Create your views here.
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.context_processors import csrf
from django.template import RequestContext
from settings import MEDIA_ROOT, MEDIA_URL
from forum.models import *
from groups.models import *
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator
import datetime

@login_required(login_url = '/login/')
def main(request):
    """Main listing."""
    lst = []
    forums = Forum.objects.all()
    for forum in forums:
        print forum.title
        num_threads = Thread.objects.filter(forum = forum)
        num_threads = len(num_threads)
        print num_threads
        lst.append((forum, num_threads))
    return render_to_response("forum/display_forums.html", dict(forums = forums, user = request.user, lst = lst))

def add_csrf(request, **kwargs):
    d = dict(user = request.user, **kwargs)
    d.update(csrf(request))
    return d

def mk_paginator(request, items, num_items):
    """Create and return a paginator."""
    paginator = Paginator(items, num_items)
    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        items = paginator.page(page)
    except (InvalidPage, EmptyPage):
        items = paginator.page(paginator.num_oages)
    return items

@login_required(login_url = '/login/')
def forum(request, pk):
    """Listing of threads in a forum"""
    print pk
    try:    
        forums = Forum.objects.all()
        forum = Forum.objects.get(pk = pk)
        threads = Thread.objects.filter(forum = pk).order_by("-created")
        print threads
        if threads.exists():
            print 'yes'
            threads = mk_paginator(request, threads, 20)
            if forum.category == 'Closed':
                grp = group.objects.get(forum = forum)
                members = groupmem.objects.filter(grp = grp)
                member = students.objects.get(studentid = request.user.username)
                for each in members:
                    if member == each.member:
                        return render_to_response("forum/display_threads.html", dict(threads = threads, pk = pk, forum = forum, forums = forums, grp = grp))
                msg = "You are not allowed to view this page"
                msg_type = "warning"
                return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})
            else:
                return render_to_response("forum/display_threads.html", dict(threads = threads, pk = pk, forum = forum, forums = forums))
        else:
            no_threads = True
            if forum.category == 'Closed':
                grp = group.objects.get(forum = forum)
                return render_to_response('forum/display_threads.html', dict(no_threads = no_threads, pk = pk, forum = forum, forums = forums, grp = grp), context_instance = RequestContext(request))
            else:
                return render_to_response('forum/display_threads.html', dict(no_threads = no_threads, pk = pk, forum = forum, forums = forums), context_instance = RequestContext(request))

    except:
        print 1
        msg = "This forum does not exist"
        msg_type = "warning"
        return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})
        


@login_required(login_url = '/login/')
def thread(request, pk):
    """Listing of posts in a thread."""
    print pk
    try:
        forums = Forum.objects.all()
        title = Thread.objects.get(pk = pk).title
        t = Thread.objects.get(pk=pk)
        if t.creator == request.user:
            admin = True
        else:
            admin = False
        print admin
        email = students.objects.get(studentid = request.user.username).emailid
        print email
        return render_to_response("forum/display_post.html",RequestContext(request, {'pk': pk,'email': email, 'admin': admin, 'title': title, 'thread_object': t, 'media_url': MEDIA_URL, 'forum_pk': t.forum.pk, 'forums': forums}))
    except:
        msg = "This thread does not exist"
        msg_type = "warning"
        return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})


def delete_thread(request, pk):
    try:
        t = Thread.objects.get(pk = pk)
        if t.creator == request.user:
            t.delete()
            return HttpResponseRedirect('/forum/')
        else:
            msg = "You are not allowed to delete this topic."
            msg_type = "warning"
            return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})
    except:
        msg = "This thread does not exist"
        msg_type = "warning"
        return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})

def post(request, ptype, pk):
    """Display a post form."""
    action = reverse("forum.views.%s" % ptype, args = [pk])
    if ptype == "new_thread":
        title = "Start new Topic"
        subject = ''
    elif ptype == "reply":
        title = "Reply"
        subject = "Re: " + Thread.objects.get(pk=pk).title

    return render_to_response("forum/post.html", dict(subject = subject, action = action, title = title))

def new_thread(request, pk):
    """Start a new thread"""
    print pk
    print 'post'
    if request.method == 'POST':
        print 'post'
        forum = Forum.objects.get(pk=pk)
        print forum.title
        print request.POST['title']
        thread = Thread(title = request.POST['title'], created = datetime.datetime.now(), creator = request.user, forum = forum)
        thread.save()
        url = '/forum/' + str(pk) + '/'
        return HttpResponseRedirect(url)
    else:
        forums = Forum.objects.all()
        forum = Forum.objects.get(pk=pk)
        return render_to_response('forum/create_thread.html', {'pk': pk, 'forum': forum, 'forums': forums})



