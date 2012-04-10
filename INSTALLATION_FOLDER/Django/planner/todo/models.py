from django.db import models
from django.utils.html import escape, escapejs  
from django.contrib.auth.models import User
from django.contrib import admin
from django.utils.translation import ugettext as _
from django.utils.encoding import force_unicode
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

# Create your models here.

class Datetime(models.Model):
    datetime = models.DateTimeField(auto_now_add = True)
    def __unicode__(self):
        return unicode(self.datetime.strftime("%b %d, %Y, %I:%M %p"))

class Item(models.Model):
    name = models.CharField(max_length = 60)
    user = models.ForeignKey(User, blank = True, null = True)
    created = models.ForeignKey(Datetime)
    priority = models.IntegerField(default = 0)
    difficulty = models.IntegerField(default = 0)
    done = models.BooleanField(default = False)
    progress = models.IntegerField(default = 0)

    def check_progress(self):
        return "<div style = 'width: 100px; border: 1px solid #ccc; '>" + "<div style = 'height: 4px; width: %dpx; background: #555; '></div></div>" %self.progress
    check_progress.allow_tags = True

    def mark_done(self):
        return "<a href = '%s'>Done</a>" % reverse("todo.views.mark_done", args = [self.pk])
    mark_done.allow_tags = True

class ItemAdmin(admin.ModelAdmin):
    list_display = ["name", "priority", "difficulty", "created", "done"]
    d=search_fields = ["name"]


class ItemInline(admin.TabularInline):
    model = Item

class DateAdmin(admin.ModelAdmin):
    list_display = ["datetime"]
    inlines = [ItemInline]

    def response_add(self, request, obj, post_url_continue='../%s/'):
        """
        Determines the HttpResponse for the add_view stage.
        """
        opts = obj._meta
        pk_value = obj._get_pk_val()

        msg = "Item(s) were added successfully" 
        # Here, we distinguish between different save types by checking for
        # the presence of keys in request.POST.
        if "_continue" in request.POST:
            self.message_user(request, msg + ' ' + _("You may edit it again below."))
            if "_popup" in request.POST:
                post_url_continue += "?_popup=1"
            return HttpResponseRedirect(post_url_continue % pk_value)

        if "_popup" in request.POST:
            return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' % \
                # escape() calls force_unicode.
                (escape(pk_value), escapejs(obj)))
        elif "_addanother" in request.POST:
            self.message_user(request, msg + ' ' + (_("You may add another %s below.") % force_unicode(opts.verbose_name)))
            return HttpResponseRedirect(request.path)
        else:
            self.message_user(request, msg)
            for item in Item.objects.filter(created = obj):
                if not item.user:
                	item.user = request.user
                	item.save()
            # Figure out where to redirect. If the user has change permission,
            # redirect to the change-list page for this object. Otherwise,
            # redirect to the admin index.
            return HttpResponseRedirect(reverse("admin:todo_item_changelist"))
