from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import reverse, render

from . import models


def return_status(status):
    resp = HttpResponse()
    resp.status_code = status
    return resp


def messages(request):
    return render(request, 'messages.html')
