from django.db import models
from datetime import datetime

# Create your models here.
class Crime(models.Model):
    eventID 			= models.CharField(max_length=20)
    callerSource 		= models.CharField(max_length=20)
    city 				= models.CharField(max_length=100)
    district 			= models.CharField(max_length=100)
    policeStation       = models.CharField(max_length=20)
    circle              = models.CharField(max_length=20)
    address             = models.CharField(max_length=200)
    zipcode				= models.IntegerField()
    latitude 			= models.CharField(max_length=20)
    longitude			= models.CharField(max_length=20)
    eventtype			= models.CharField(max_length=100)
    eventsubtype		= models.CharField(max_length=100)
    datetime			= models.DateTimeField(default=datetime.now,blank=True)

    class Meta:
        ordering = ['city','policeStation','datetime']
        # verbose_name_plural = 'Crime'