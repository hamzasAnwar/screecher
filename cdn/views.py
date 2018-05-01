from django.http import HttpResponse
from django.db import connections

import json


def user_info(request, profile_id):
    cursor = connections['default'].cursor()
    cursor.execute("SELECT first_name, last_name, username, email FROM screecher_userprofile WHERE id=%s", (profile_id,))
    user_profile = cursor.fetchone()
    if user_profile is None:
        return HttpResponse('')
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
    # Allow only certain domains and what might happen if proxies get in the way
    parent_origin = '.'.join(request.META.get('HTTP_ORIGIN').split('.')[1:])
    parent_host = '.'.join(request.META.get('HTTP_HOST').split('.')[1:])
    if parent_origin in [parent_host, 'null']:
        response['Access-Control-Allow-Origin'] = request.META.get('HTTP_ORIGIN')
    response['Access-Control-Allow-Credentials'] = 'true'
    return response


