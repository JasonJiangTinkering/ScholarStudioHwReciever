from django.conf.urls import url
from django.http.response import HttpResponse
from django.shortcuts import render
from django.template import RequestContext
from .forms import hw1, glitchHw
from .models import Student, Assignment, Glitchassignment
from django.http import HttpResponseRedirect
from annoying.functions import get_object_or_None
# Create your views here.
def index(request):
    if request.method == "POST":
        form = hw1(request.POST, request.FILES)
        if form.is_valid():
            thisStudent = get_object_or_None(Student, email=form.cleaned_data['email'])
            if thisStudent and not thisStudent.assignment_set.filter(hwNumber=1).exists():
                thisStudent.assignment_set.create(hwNumber = 1, image = form.cleaned_data['file'])
                return HttpResponse('file submitted') 
            else:
                return HttpResponse('file already submitted or student not found') 
        print(form.errors)
        
    context = {
        'form' : hw1()
    }
    return render(request, 'frontend/index.html', context)

def glitchsubmit(request):
    if request.method == "POST":
        form = glitchHw(request.POST);
        if form.is_valid():
            thisStudent = get_object_or_None(Student, email=form.cleaned_data['email'])
            if thisStudent:
                if (not thisStudent.glitchassignment_set.filter(hwNumber=2).exists()):
                    thisStudent.glitchassignment_set.create(hwNumber =2, url = form.cleaned_data['url'])
                    return HttpResponse('file submitted') 
                else:
                    return HttpResponse('ERROR: file already submitted')     
            else:
                return HttpResponse('ERROR: student not found') 
    context = {
        'form' : glitchHw(),
        "type": "glitch"
    }
    return render(request, 'frontend/index.html', context)
    

def view(request, day):
    context = {}
    learners = {}
    for bud in Student.objects.all():
        try:
            if (day == 1):
                result = bud.assignment_set.get(hwNumber=day)
                context["view"] = "image"
            else:
                result = bud.glitchassignment_set.get(hwNumber=day)
                
                result = result.url
                print(result)
                result = result[:result.find('.')]
                result = result[result.rfind('/') + 1:]
                context["view"] = "glitch"
            if (bud.name):
                learners[bud.name] = result
            else:
                learners[bud.email] = result
        except:
            if (bud.name):
                learners[bud.name] = False
            else:
                learners[bud.email] = False
    context["students"] = learners
    context["day"] = day
    print(context)
    return render(request, 'frontend/view.html', context)

