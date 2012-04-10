from django.db import models
from usrper.models import students
# this table consists of the tables required by the application of a group 
#with the functionality as follows:
# it can create a group and decide the members and the events concerning the group
# Create your models here.
class group(models.Model):
   agenda = models.TextField(max_length=50)
   id = models.AutoField(primary_key=True)
   groupadmin = models.IntegerField()

class groupmem(models.Model):
   member = models.ForeignKey(students)
   grp = models.ForeignKey(group)
#   groupadmin = models.OneToOneField(students)
#class group_ag(models.Model):
#	agenda = models.TextField(max_length=50)
#	groupid = models.ForeignKey(group_adm)
#class group_mem(models.Model):
#	members = models.ManyToManyField(students)
#	groupid = models.ForeignKey(group_adm)

class groupupdates(models.Model):
	grp =models.ForeignKey(group)#OneToOneField(group_adm)
	event = models.TextField()
	updtby = models.IntegerField()

class groupreq(models.Model):
	grp = models.ForeignKey(group)
	member = models.ForeignKey(students)

class groupevent(models.Model):
    grp = models.ForeignKey(group)
    event = models.IntegerField()
    
class groupeventmembers(models.Model):
    group_event = models.ForeignKey(groupevent)
    member = models.ForeignKey(students)

class groupeventrequests(models.Model):
    group_event = models.ForeignKey(groupevent)
    member = models.ForeignKey(students)

#end
