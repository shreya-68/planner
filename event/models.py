from django.db import models

class Event_Type(models.Model):
    EVENT_CHOICES = (
            (u'P', 'Project'),
            (u'C', 'Club'),
            (u'L', 'Lecture'),
            (u'A', 'Assignment'),
            (u'O', 'Other'),
    )
    event = models.CharField(max_length=2, choices=EVENT_CHOICES)
    priority = models.IntegerField()
    def __unicode__(self):
        return self.get_event_display()

class Project(models.Model):
    course = models.CharField(max_length=5)
    event_type = models.ForeignKey(Event_Type)
    last_date = models.DateTimeField()
#    event = models.ForeignKey(Events)
    duration = models.FloatField()
    complete = models.FloatField()
    USER_DIFF_CHOICES = (
            (1,1),
            (2,2),
            (3,3),
            (4,4),
            (5,5),
    )       
    user_difficulty = models.IntegerField(choices=USER_DIFF_CHOICES)


class Club(models.Model):
    name = models.CharField(max_length=40)
    event = models.CharField(max_length=40)
    e_time = models.DateTimeField()
    venue = models.CharField(max_length=70)
 #   event = models.ForeignKey(Events)
    duration = models.FloatField()
    complete = models.FloatField()
    USER_DIFF_CHOICES = (
            (1,1),
            (2,2),
            (3,3),
            (4,4),
            (5,5),
    )       
    user_difficulty = models.IntegerField(choices=USER_DIFF_CHOICES)
    
class Lecture(models.Model):
    ltiming = models.DateTimeField()
    SLOT_CHOICES = (
            (1, 1),
            (2,2),
            (3,3),
            (4,4),
            (5,5),
            (6,6),
            (7,7),
            (8,8),
    )
  #  event = models.ForeignKey(Events)
    slot = models.IntegerField(choices=SLOT_CHOICES)
    duration = models.FloatField()
    complete = models.FloatField()
    USER_DIFF_CHOICES = (
            (1,1),
            (2,2),
            (3,3),
            (4,4),
            (5,5),
    )       
    user_difficulty = models.IntegerField(choices=USER_DIFF_CHOICES)

class Other(models.Model):
    name = models.CharField(max_length=40)
    time = models.DateTimeField()
   #duration = models.FloatField()
   #event = models.ForeignKey(Events)
    duration = models.FloatField()
    complete = models.FloatField()
    #USER_DIFF_CHOICES = (
     #       (1,1),
      #      (2,2),
       #     (3,3),
        #    (4,4),
         #   (5,5),
    #)       
    #user_difficulty = models.IntegerField(choices=USER_DIFF_CHOICES)

# Create your models here.
