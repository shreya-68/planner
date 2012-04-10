# Create your views here.
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from settings import MEDIA_ROOT, MEDIA_URL
from forum.models import *
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator
import datetime

@login_required(login_url = '/login/')
def main(request):
    """Main listing."""
    forums = Forum.objects.all()
    return render_to_response("forum/display_forums.html", dict(forums = forums, user = request.user))

#def add_csrf(request, **kwargs):
#    d = dict(user = request.user, **kwargs)
#    d.update(csrf(request))
#    return d

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
@csrf_exempt
def forum(request, pk):
    """Listing of threads in a forum"""
    print pk
    forum = Forum.objects.get(pk = pk)
    threads = Thread.objects.filter(forum = pk).order_by("-created")
    threads = mk_paginator(request, threads, 20)
    return render_to_response("forum/display_threads.html", dict(threads = threads, pk = pk, forum = forum))

@login_required(login_url = '/login/')
@csrf_exempt
def thread(request, pk):
    """Listing of posts in a thread."""
    print pk
    title = Thread.objects.get(pk = pk).title
    t = Thread.objects.get(pk=pk)
    return render_to_response("forum/display_post.html", {'pk': pk, 'title': title, 'thread_object': t, 'media_url': MEDIA_URL, 'forum_pk': t.forum.pk})

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

@csrf_exempt
def new_thread(request, pk):
    """Start a new thread"""
    print pk
    print 'post'
    if request.method == 'POST':
    	print 'post'
        forum = Forum.objects.get(pk=pk)
        print forum.title
        print request.method['title']
        thread = Thread(title = request.method['title'], created = datetime.datetime.now(), creator = request.user, forum = forum)
        thread.save()
        msg = "New topic created successfully"
        msg_type = 'success'
        return render_to_response('notify/notify.html', {'msg': msg, 'msg_type': msg_type})
    else:
        forum = Forum.objects.get(pk=pk)
        return render_to_response('forum/create_thread.html', {'pk': pk, 'forum': forum})


def reply(request, pk):
    """Reply to a thread"""
    p = request.POST
    if p["body"]:
    	thread = Thread.objects.get(pk=pk)
    	post = Post.objects.create(thread = thread, title = p["subject"], body = p["body"], creator = request.user)
    return HttpResponseRedirect(reverse("forum.views.thread", args = [pk]) + "?page=last")

