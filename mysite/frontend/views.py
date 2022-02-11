from django.conf.urls import url
from django.urls import reverse
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.template import RequestContext
from .forms import hw1, glitchHw, InitChallengerForm
from .models import Student, Assignment, Glitchassignment, PresetChallenger, GameChallenger
from django.http import HttpResponseRedirect
from annoying.functions import get_object_or_None
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timezone
import datetime as datetimeparent
import json
def game_homepage(request):
    if request.method == 'POST':
        f = InitChallengerForm(request.POST);
        if f.is_valid():
            print("Challenger's Code:" + str(f.cleaned_data['code']))
            foundPreset = None
            try:
                foundPreset = PresetChallenger.objects.get(player_code=f.cleaned_data['code'])
            except ObjectDoesNotExist:
                print("Code does not exist")
            challenger = f.save()
            foundPreset.GameChallenger = challenger
            foundPreset.save()
            return redirect(reverse('game_go', args=[getattr(challenger, 'code')]))
    context = {
        'form' : InitChallengerForm()
    }
    return render(request, 'frontend/game_homepage.html', context)
def game_post(request):
    if request.method == 'POST':
        # reject if spectating
        data = request.read().decode('ascii')
        print("Post Request recieved from" + data)
        challenger = GameChallenger.objects.get(code=data)
        if challenger.time_started is None:
            challenger.time_started = datetime.now()
        challenger.latest_time = datetime.now()
        challenger.save();
        totaltime = 0
        for i in GameChallenger.objects.all().iterator():
            totaltime += i.time_held()
        outrequest = {
            "time_held": challenger.time_held(),
             "total_time": totaltime,
        }
        return HttpResponse(json.dumps(outrequest))


def game_go(request, code):
    # test if event has started
    challenger = GameChallenger.objects.get(code=code)
    if challenger.logged_in:
        print("Player " + code + " has relogged in")
        # you may no longer play
        challenger.presetchallenger.active = False
        challenger.save()
    else:
        print("Player " + code + " has logged in")
        challenger.logged_in = True
        challenger.save()
    print("now" + str(type(datetime.now(timezone.utc))) + " : " + str(type(challenger.presetchallenger.event_end)))
    print("now" + str(datetime.now(timezone.utc)) + " : " + str(challenger.presetchallenger.event_end))
    start_time = datetime.now().time()
    stop_time = challenger.presetchallenger.event_end
    print(start_time)
    date = datetimeparent.date(1, 1, 1)
    datetime1 = datetime.combine(date, start_time)
    datetime2 = datetime.combine(date, stop_time)
    time_left = datetime1 - datetime2
    print(time_left)
    context = {
        "player": challenger,
        "time_left": time_left
    }
    return render(request, 'frontend/game_go.html', context)

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
