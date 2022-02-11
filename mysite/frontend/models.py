from django.db import models
# from django.forms.fields import EmailField, ImageField
# from django.forms.widgets import NumberInput
from datetime import datetime, timezone
import datetime as datetimeparent
import math
# Create your models here.s
class Student(models.Model):
    name = models.CharField(default ="", blank=True, max_length=255)
    email = models.EmailField()
    REQUIRED_FIELDS = ['email']

class Assignment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    hwNumber = models.IntegerField()
    image = models.ImageField(upload_to='images')
    REQUIRED_FIELDS = ['student', 'hwNumber', 'image']


class Glitchassignment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    hwNumber = models.IntegerField()
    url = models.URLField(max_length=200)
    REQUIRED_FIELDS = ['student', 'hwNumber', 'url']

# create the challengers prior to the event
class PresetChallenger(models.Model):
    event_start = models.TimeField()
    event_end = models.TimeField()
    active = models.BooleanField(default=True)
    player_code = models.IntegerField()
    GameChallenger = models.OneToOneField(
        "GameChallenger", on_delete=models.CASCADE, null=True, blank=True
    ) # connect with the challenger

    REQUIRED_FIELDS = ['event_start', 'event_end', 'player_code']

class GameChallenger(models.Model):
    name = models.CharField(blank=False, max_length=50)
    code = models.IntegerField()
    lockernumber = models.IntegerField()
    dietary_restrictions = models.TextField(blank=True)
    logged_in = models.BooleanField(default=False)
    time_started = models.TimeField(null=True, blank=True) #set during first instance of add latest time
    latest_time = models.TimeField(null=True, blank=True) #set at every http request to the server
    REQUIRED_FIELDS = ['name', 'code', 'lockernumber']

    # time started
    def time_held(self):
        print("TIMES:"+str(self.latest_time) +':' +str(self.time_started))
        x =str(self.latest_time)
        y= str(self.time_started)
        if " " in x:
            throw, throw,x = x.partition(" ")

        if " " in y:
            throw, throw,y = y.partition(" ")
        x = x.split(':')
        y= y.split(':')

        time = 0
        time += (int(x[-3])-int(y[-3]))*3600
        time += (int(x[-2])-int(y[-2]))*60
        time += math.floor(float(x[-1])-float(y[-1]))
        return time
        # date = datetimeparent.datetime(1, 1, 1)
        # datetime1 = datetime.combine(date, self.time_started)
        # datetime2 = datetime.combine(date, self.latest_time)
        # time_left = datetime1 - datetime2
        # start_time = start_time.strftime('%H:%M')

        # time_left = self.latest_time - self.time_started
        # return time_left.total_seconds()
