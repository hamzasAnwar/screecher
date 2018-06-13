from django.http import HttpResponse
from django.shortcuts import render
from pymongo import MongoClient


def return_status(status):
    resp = HttpResponse()
    resp.status_code = status
    return resp


def premium_area(request):
    access = request.POST.get('access', None)
    if access is None:
        return render(request, 'premium.html', context={'access': False})
    search = 'function(){return (this.secret==encodeURI("%s"))}' % access
    db = MongoClient('localhost', 27017).secrets
    auth = db.secret.find_one({'$where': search})
    if auth is None:
        return return_status(418)
    return render(request, 'premium.html', context={'access': True})

