import base64
import hashlib
import random
import string

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.safestring import mark_safe

from friendcdn.models import FriendshipRequest, User


def generate_nonce(length=8):
    """Generate pseudorandom nonce."""
    return ''.join([str(random.randint(0, 9)) for i in range(length)])


@login_required
def friend_list(request):
    own_domain = '.'.join(request.META.get('HTTP_HOST').split('.')[1:])
    pending_requests = FriendshipRequest.objects.filter(requested=request.user)
    response = render(request, 'friends.html',
                      context={'own_domain': own_domain,
                               'messages': messages.get_messages(request),
                               'pending_requests': pending_requests})
    return response


@login_required
def view_friend_request(request):
    username = request.GET.get("user")
    own_domain = '.'.join(request.META.get('HTTP_HOST').split('.')[1:])

    if username is None:
        messages.warning(request, "Given a user name please")
        return HttpResponseRedirect("/friends")

    try:
        new_friend = User.objects.get(username=username)
    except ObjectDoesNotExist:
        messages.warning(request, "No such user")
        return HttpResponseRedirect("/friends")

    try:
        fsr = FriendshipRequest.objects.get(requested=request.user, requester=new_friend)
    except ObjectDoesNotExist:
        messages.warning(request, "No such friendship request")
        return HttpResponseRedirect("/friends")

    fsr.message = mark_safe(fsr.message)

    # dynamically generate a nonce
    nonce = base64.b64encode(generate_nonce(8).encode("utf-8")).decode("utf-8")

    allowed_sources = ["'self'",
                       "'sha256-I+x1DjCE8PdmvoLRVq88w0XijGbAptyttYCK8Rv+dZw='",  # friendship functions
                       "'sha256-As7HfO77CaHa0fpRw/BdrTBrsMThnqVkBKnS6BgFCAM='",  # jQuery check
                       "'sha256-odhnBeDHBp5KbGdKxa2XBs+4F9uaYMQB5gL5MBmzgsM='",  # translate feature
                       "'nonce-%s'" % nonce,
                       "https://cdnjs.cloudflare.com/ajax/libs/tether/1.4.0/js/tether.min.js",
                       "https://code.jquery.com/jquery-3.3.1.min.js",
                       "https://cdn.%s" % own_domain  # CDNs hosts important configurations

                       ]

    response = render(request, 'friendshiprequest.html',
                      context={'own_domain': own_domain,
                               'messages': messages.get_messages(request),
                               'fsr': fsr,
                               'nonce': nonce})
    response["Content-Security-Policy"] = "script-src " + " ".join(allowed_sources)
    return response
