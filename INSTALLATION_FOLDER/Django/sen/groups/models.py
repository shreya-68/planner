from django.db import models
from sen.usrper.models import students
# this table consists of the tables required by the application of a group 
#with the functionality as follows:
# it can create a group and decide the members and the events concerning the group
# Create your models here.
class group(models.Model):
   agenda = models.TextField(max_length=50)
   id = models.AutoField(primary_key=True)
   groupadmin = models.IntegerField()
class groupmem(models.Model):
   members = models.ForeignKey(students)
   groupid = models.ForeignKey(group)
#   groupadmin = models.OneToOneField(students)
#class group_ag(models.Model):
#	agenda = models.TextField(max_length=50)
#	groupid = models.ForeignKey(group_adm)
#class group_mem(models.Model):
#	members = models.ManyToManyField(students)
#	groupid = models.ForeignKey(group_adm)
class groupupdates(models.Model):
	grpid =models.ManyToManyField(group)#OneToOneField(group_adm)
	event = models.TextField()
	updtby = models.IntegerField()
class groupreq(models.Model):
	grp = models.ForeignKey(group)
	stdrqstd = models.ForeignKey(students)
#end
