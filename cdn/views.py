from django.http import HttpResponse
from django.db import connections

import json

def is_allowed_origin(http_origin, http_host):
    # allow www.teamX access
    if http_origin:
        # strip SSL
        http_origin = http_origin.replace("https://", "")
        if http_origin.startswith("www.team") and http_origin.replace("www.", "cdn.") == http_host:
            return True
    # allow access if proxy nullifies the header for privacy reasons
    if http_origin == 'null':
        return True
    return False


def user_info(request):
    if request.user.id is None:
        return HttpResponse("Sorry, not logged in.")
    cursor = connections['default'].cursor()
    cursor.execute("SELECT first_name, last_name, username, email FROM screecher_userprofile WHERE user_id=%s", (request.user.id,))
    user_profile = cursor.fetchone()
    if user_profile is None:
        return HttpResponse('No such user ID!')
    first_name, last_name, username, email = user_profile
    data = {
        'first_name': first_name,
        'last_name': last_name,
        'username': username,
        'email': email
    }
    response = HttpResponse(json.dumps(data))
    response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
    response['Access-Control-Allow-Headers'] = '*'
    response['Access-Control-Max-Age'] = 42
    if is_allowed_origin(request.META.get('HTTP_ORIGIN'), request.META.get('HTTP_HOST')):
        response['Access-Control-Allow-Origin'] = request.META.get('HTTP_ORIGIN')
    response['Access-Control-Allow-Credentials'] = 'true'
    return response


