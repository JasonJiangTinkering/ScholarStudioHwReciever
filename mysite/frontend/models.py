from django.db import models
# from django.forms.fields import EmailField, ImageField
# from django.forms.widgets import NumberInput

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
    player_code = models.IntegerField()
    REQUIRED_FIELDS = ['event_start', 'event_end', 'player_code']

class GameChallenger(models.Model):
    name = models.CharField(blank=False, max_length=50)
    code = models.IntegerField()
    lockernumber = models.IntegerField()
    dietary_restrictions = models.TextField(blank=True)
    logged_in = models.BooleanField()
    time_started = models.TimeField() #set during first instance of add latest time
    latest_time = models.TimeField() #set at every http request to the server
    PresetChallenger = models.OneToOneField(
        PresetChallenger, on_delete=models.PROTECT
        ) # connect with the settings of the challenger
    REQUIRED_FIELDS = ['name', 'code', 'lockernumber']

    # time started
