from django.db import models
#this file has user's personal information as well as academic info of a user
# Create your models here.
class students(models.Model):
   name = models.TextField()
   emailid = models.EmailField()
   roomno = models.IntegerField()
   phonenumber = models.IntegerField()
   sleephours = models.TimeField('%H:%M')
   lunchtime = models.TimeField('%H:%M')
   dinnertime = models.TimeField('%H:%M')
   waketime = models.TimeField('%H:%M')
   hobbies = models.TextField()
   cpi = models.IntegerField()
   cursem = models.IntegerField()
   Year = models.IntegerField()
   studentid = models.IntegerField(primary_key=True)
   cemailid =models.EmailField()
   max_eff = models.TimeField() 

class userhascourses(models.Model):
   studentid = models.ForiegnKey('students.studentid')
   courseic = models.ForiegnKey('courses.courseid')

# table showing the projectrelationtostudent
class stdtopro(models.Model):
   projectname = models.TextField()
   members = models.ForiegnKey('student.studentid')
   diffbyuser = models.ChoiceField()		#requires list of difficulty levels
   prodis = models.TextField()
