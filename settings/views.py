from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from django.template.defaultfilters import register
from django.utils.safestring import mark_safe as encode_param

from screecher.models import UserProfile
from . import models

import json

@register.simple_tag
def encode_string(string):
    return encode_param(string)


def return_status(status):
    resp = HttpResponse()
    resp.status_code = status
    return resp


@login_required
def settings_page(request):
    profile = UserProfile.objects.get(id=1)#user=request.user)
    return render(request, 'settings.html', {'profile': profile})


@login_required
def change_profile(request):
    profile = UserProfile.objects.get(user=request.user)
    first_name = request.POST.get('new_first')
    if first_name is not None:
        profile.first_name = first_name
    last_name = request.POST.get('new_last')
    if last_name is not None:
        profile.last_name = last_name
    mail = request.POST.get('new_mail')
    if mail is not None:
        profile.mail = mail
    profile.save()
    return return_status(200)


def tracking(request):
    return render(request, 'tracking.html')


def logging(request):
    #try:
    data = json.loads(request.body.decode('utf-8'))
    user_id = data["user_id"]
    visited_page = data["page"]
    #except:
    #    return return_status(418)
    models.PageLog.objects.create(user_id=user_id, page=visited_page).save()
    return return_status(200)