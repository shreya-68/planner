from django.db import models
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib import admin
from string import join
from settings import MEDIA_ROOT

# Create your models here.

class Forum(models.Model):
    title = models.CharField(max_length = 60)
    def __unicode__(self):
        return self.title
    
    def num_posts(self):
        return sum([t.num_posts() for t in self.thread_set.all()])

    def last_post(self):
        if self.thread_set.count():
        	last = None
        	for t in self.thread_set.all():
        		l = t.last_post()
        		if l:
        			if not last: last = l
        			elif l.created > last.created: last = l
        	return last

class Thread(models.Model):
    title = models.CharField(max_length = 60)
    created = models.DateTimeField(auto_now_add = True)
    creator = models.ForeignKey(User, blank = True, null = True)
    forum = models.ForeignKey(Forum)

    def __unicode__(self):
        return unicode(self.creator) + " - " + self.title

    def num_posts(self):
        return self.post_set.count()

    def num_replies(self):
        return self.post_set.count() - 1

    def last_post(self):
        if self.post_set.count():
        	return self.post_set.order_by("created")[0]

class Post(models.Model):
    title = models.CharField(max_length = 60)
    created = models.DateTimeField(auto_now_add = True)
    creator = models.ForeignKey(User, blank = True, null = True)
    thread = models.ForeignKey(Thread)
    body = models.TextField(max_length = 10000)

    def __unicode__(self):
        return u"%s - %s - %s" % (self.creator, self.thread, self.title)

    def short(self):
        return u"%s - %s\n%s" % (self.creator, self.title, self.created.strftime("%b %d, %I:%M %p"))
    short.allow_tags = True

# Admin
#

class ThreadForm(ModelForm):
    title = forms.CharField(max_length = 60)
    class Meta:
        model = Thread
        fields = ('title',)


class ForumAdmin(admin.ModelAdmin):
    pass

class ThreadAdmin(admin.ModelAdmin):
    list_display = ["title", "forum", "creator", "created"]
    list_filter = ["forum", "creator"]
    
class PostAdmin(admin.ModelAdmin):
    seaarch_fields = ["title", "creator"]
    list_display = ["title", "thread", "creator", "created"]


