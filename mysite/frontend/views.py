from django.http.response import HttpResponse
from django.shortcuts import render
from django.template import RequestContext
from .forms import hw1
from .models import Student, Assignment
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

def view(request, day):
    context = {}
    learners = {}
    for bud in Student.objects.all():
        try:
            result = bud.assignment_set.get(hwNumber=day)
            learners[bud.email] = result
        except:
            learners[bud.email] = False
    context["students"] = learners
    context["day"] = day
    return render(request, 'frontend/view.html', context)

