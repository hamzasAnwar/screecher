from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection


def return_status(status):
    resp = HttpResponse()
    resp.status_code = status
    return resp


@login_required
def profile_search(request):
    username = request.POST.get("user", None)
    if username is None:
        return return_status(418)
    with connection.cursor() as cursor:
        query = "SELECT username FROM auth_user WHERE auth_user.username=%s;"
        cursor.execute(query,(username,))
        profile = cursor.fetchone()
        return render(request, 'search.html', context={'search_profiles': profile})


@login_required
def feedback(request):
    data = {'user': request.user.username}
    return render(request, 'feedback.html', context=data)


@login_required
def save_feedback(request):
    comment = request.POST.get("comment", None)
    user = request.POST.get("user", None)
    if comment is None or user is None:
        return return_status(418)
    with connection.cursor() as cursor:
        query = "INSERT INTO dbtests_feedback (username, content) VALUES ('%s', '%s');"
        _ = cursor.execute(query % (user, comment,))
        return return_status(200)
