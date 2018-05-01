from django.http import HttpResponse
from django.shortcuts import render

from .models import Advertisement
import random
import hashlib
import json

ads_templates = ['snow-owl.html', 'feathers.html', 'lootbox.html', 'ads.html']


def return_status(status):
    resp = HttpResponse()
    resp.status_code = status
    return resp


def ad_service(request):
    rng = random.randint(0, len(ads_templates) - 1)
    return render(request, ads_templates[rng])


def ad_count(request):
    if request.method == 'POST':
        token = request.POST.get('ad_token', None)
        ad_host = request.POST.get('ad_host', None)
        if token is None or ad_host is None:
            return return_status(418)
        host_hash = hashlib.sha256(ad_host.encode('utf-8')).hexdigest()
        try:
            ad = Advertisement.objects.get(token=token, host=host_hash)
            ad.loaded = ad.loaded + 1
        except Advertisement.DoesNotExist:
            ad = Advertisement.objects.create(token=token, host=host_hash, loaded=1)
        ad.save()
        response = return_status(202)
        response['Access-Control-Allow-Headers'] = '*'
        response['Access-Control-Max-Age'] = 12345678
        response['Access-Control-Allow-Origin'] = '*'
        return response
    elif request.method == 'GET':
        curr_count = {}
        ads = Advertisement.objects.all()
        for ad in ads:
            if ad.host not in curr_count:
                curr_count[ad.host] = {}
            curr_count[ad.host][ad.token] = ad.loaded
        return HttpResponse(json.dumps(curr_count))
    else:
        return return_status(401)


