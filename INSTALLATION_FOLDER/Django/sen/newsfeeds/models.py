from django.db import models

# Create your models here.
class feeds(models.Model):
    newsfeed = models.TextField()
    posted_on = models.DateTimeField()
    added_by = models.IntegerField()
