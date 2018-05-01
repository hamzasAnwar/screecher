from django.contrib.auth import authenticate, logout, login as auth_login
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, reverse
from django.contrib.auth.models import User

from . import models


def return_status(status):
    resp = HttpResponse()
    resp.status_code = status
    return resp


def registration(request):
    username = request.POST.get('user', None)
    password = request.POST.get('pwd1', None)
    email = request.POST.get('email', None)
    user = User.objects.create_user(username=username, password=password)
    if user is not None:
        user.save()
        user_profile = models.UserProfile()
        user_profile.username = username
        user_profile.email = email
        user_profile.user = user
        user_profile.save()
        auth_login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        return_status(500)


def login_view(request):
    user = request.POST.get('user', None)
    pwd = request.POST.get('pwd', None)
    if user is None or pwd is None:
        return return_status(401)
    user = authenticate(request=request, username=user, password=pwd)
    if user is not None and user.is_active:
        auth_login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        return return_status(401)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def profile(request, profile_id):
    own_domain = '.'.join(request.META.get('HTTP_HOST').split('.')[1:])
    return render(request, 'profile.html', {"profile_id": profile_id, 'own_domain': own_domain})

