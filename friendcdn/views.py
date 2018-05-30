from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.utils.safestring import mark_safe

from . import models


def return_status(status):
    resp = HttpResponse()
    resp.status_code = status
    return resp


@login_required
def accept_requested_friend(request):
    to_friend = request.POST.get("new_friend")

    own_domain = '.'.join(request.META.get('HTTP_HOST').split('.')[1:])
    friends_page = "https://www." + own_domain + "/friends"

    if to_friend is None:
        messages.warning(request, "You must post a friend")
        return HttpResponseRedirect(friends_page)

    try:
        new_friend = models.User.objects.get(username=to_friend)
    except ObjectDoesNotExist:
        messages.warning(request, "No such user")
        return HttpResponseRedirect(friends_page)

    try:
        fsr = models.FriendshipRequest.objects.get(requester=new_friend, requested=request.user)
    except ObjectDoesNotExist:
        messages.warning(request, "No pending friendship request for these")
        return HttpResponseRedirect(friends_page)

    fs, created = models.Friendship.objects.get_or_create(user1=request.user, user2=new_friend)
    if created:
        fs.save()
        messages.success(request, "Friend successfully added")
    else:
        messages.success(request, "You already were friends?")

    fsr.delete()
    return HttpResponseRedirect(friends_page)


@login_required
def add_request_friend(request):
    to_friend = request.POST.get("new_friend")
    message = request.POST.get("message")

    own_domain = '.'.join(request.META.get('HTTP_HOST').split('.')[1:])
    friends_page = "https://www." + own_domain + "/friends"

    if to_friend is None or message is None:
        messages.warning(request, "You must post a friend and message")
        return HttpResponseRedirect(friends_page)

    try:
        new_friend = models.User.objects.get(username=to_friend)
    except ObjectDoesNotExist:
        messages.warning(request, "No such user")
        return HttpResponseRedirect(friends_page)

    if new_friend == request.user:
        messages.warning(request, "Do you not have any real friends? Adding yourself is pointless")
        return HttpResponseRedirect(friends_page)

    obj, created = models.FriendshipRequest.objects.get_or_create(requested=new_friend, requester=request.user)
    obj.message = message
    obj.save()
    if created:
        messages.success(request, "Friendship requested created")
        return HttpResponseRedirect(friends_page)
    else:
        messages.success(request, "Friendship requested updated")
        return HttpResponseRedirect(friends_page)

@login_required
def add_friend(request):
    to_friend = request.POST.get("new_friend")
    csrftoken = request.POST.get("csrftoken")

    own_domain = '.'.join(request.META.get('HTTP_HOST').split('.')[1:])
    friends_page = "https://www." + own_domain + "/friends"

    if to_friend is None:
        messages.warning(request, "No friend passed to endpoint")
        return HttpResponseRedirect(friends_page)
    if csrftoken == request.session['csrftoken']:
        try:
            new_friend = models.User.objects.get(username=to_friend)
        except ObjectDoesNotExist:
            messages.warning(request, "No such user")
            return HttpResponseRedirect(friends_page)
        if new_friend == request.user:
            messages.warning(request, "Do you not have any real friends? Adding yourself is pointless")
            return HttpResponseRedirect(friends_page)
        try:
            models.Friendship.objects.create(user1=request.user, user2=new_friend).save()
        except Exception as e:
            messages.warning(request, "Adding friend failed, duplicate? " + str(e))
            return HttpResponseRedirect(friends_page)
        messages.success(request, "Added %s as a friend" % (to_friend, ))
        return HttpResponseRedirect(friends_page)
    messages.warning(request,"Error :(")
    return HttpResponseRedirect(friends_page)

@login_required
def friend_script(request):
    friendships = models.Friendship.objects.filter(user2=request.user)
    session_token = request.session["friendtoken"]
    url_token = request.GET.get("friendtoken")

    if session_token == url_token:
        friends = []
        for f in friendships:
            friends.append(f.user1.username)
        return render(request, 'friend_script.js',
                      context={'friends': friends, 'cb': mark_safe(request.GET.get("cb", "console.log"))},
                      content_type="application/x-javascript")
