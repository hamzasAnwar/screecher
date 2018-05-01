from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import reverse, render

from . import models


def return_status(status):
    resp = HttpResponse()
    resp.status_code = status
    return resp


def index(request):
    if request.user.is_authenticated:
        screeches = models.Screech.objects.filter(user=request.user)
        return render(request, 'home.html', context={'screeches': screeches})
    else:
        return render(request, 'landing.html')


def screech(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            models.Screech.objects.create(user=request.user, content=request.POST['screech_area']).save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return return_status(500)
    else:
        return return_status(403)
