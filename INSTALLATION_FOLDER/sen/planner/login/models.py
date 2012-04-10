from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User)
#other fields here:
    roomno = models.IntegerField(null=True)
	phonenumber = models.IntegerField()
	sleephours = models.TimeField('%H:%M',null=True)
	lunchtime = models.TimeField('%H:%M',null=True)
	dinnertime = models.TimeField('%H:%M',null=True)
	usualwakingtime = models.TimeField('%H:%M',null=True)
	hobbies = models.TextField(null=True)
	cpi = models.IntegerField(null=True)
	cursem = models.IntegerField(null=True)
	Year = models.IntegerField(null = True)
	studentid = models.IntegerField(primary_key=True)
	cemailid =models.EmailField()

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
        	UserProfile.objects.create(user=instance)
    
    post_save.connect(create_user_profile, sender=User)

# table showing the projectrelationtostudent
class stdtopro(models.Model):
	projectname = models.TextField()
	members = models.OneToOneField(students)
	diffbyuser = models.IntegerField()		#requires list of difficulty levels
	prodis = models.TextField()


