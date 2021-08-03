from django.db import models
from django.forms.fields import EmailField, ImageField
from django.forms.widgets import NumberInput

# Create your models here.
class Student(models.Model):
    name = models.CharField(default ="", max_length=255)
    email = models.EmailField()

class Assignment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    hwNumber = models.IntegerField()
    image = models.ImageField(upload_to='images')