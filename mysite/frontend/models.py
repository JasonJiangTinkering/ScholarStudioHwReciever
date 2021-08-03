from django.db import models
from django.forms.fields import EmailField, ImageField
from django.forms.widgets import NumberInput

# Create your models here.
class Student(models.Model):
    name = models.CharField(default ="", blank=True, max_length=255)
    email = models.EmailField()
    REQUIRED_FIELDS = ['email']

class Assignment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    hwNumber = models.IntegerField()
    image = models.ImageField(upload_to='images')
    REQUIRED_FIELDS = ['student', 'hwNumber', 'image']