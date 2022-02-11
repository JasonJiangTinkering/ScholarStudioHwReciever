from django.contrib import admin
from .models import Student, Assignment, Glitchassignment, GameChallenger, PresetChallenger
# Register your models here.

admin.site.register(Student)
admin.site.register(Assignment)
admin.site.register(Glitchassignment)
admin.site.register(GameChallenger)
admin.site.register(PresetChallenger)
