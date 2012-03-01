from django.db import models
# this table consists of the tables required by the application of a group 
#with the functionality as follows:
# it can create a group and decide the members and the events concerning the group
# Create your models here.
class group(models.Model):
members = models.ForiegnKey('students.student_id')
agenda = models.TextField()
groupid = models.IntegerField(primary_key=True)

#class groupupdates(models.Model):
#groupid =models.ForiegnKey('group.groupid')
event = models.TextField()
#end
