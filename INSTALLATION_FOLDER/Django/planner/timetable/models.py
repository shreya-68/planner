from django.db import models
#this table is for creating a timetable which is specific to a user
# Create your models here.
class ttable(models.Model):
    stime = models.TimeField('%H:%M')
    sptime = models.TimeField('%H:%M')
    slotnum = models.ForiegnKey('courses.slotid')
    day= models.TextField()

class courses(models.Model):
    courseid = models.CharField(max_length = 5)
    instid = models.DecimalField()
    slotid = models.IntegerField()
    coursedis = models.TextField()
    coursename = models.Textfield()

class coursetostd(models.Model):
    studentid = models.ForiegnKey('students.studentid')
    courseid = models.ForiegnKey('courses.courseid')

class labttable(models.Model):
    labstime = models.TimeField()
    labstptime = models.TimeField()
    Courseid models.Foriegnkey('courses.courseid')
    labgrpid =models.ForiegnKey('students.labgrpid')
    labday = models.TextField()

