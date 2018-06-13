from base64 import b64encode, b64decode

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from hashlib import sha256

from django.template import Template, Context

from . import models

from socialnetwork import settings

import datetime
import pickle

err_wallet = """
<html>
<title>404</title>
<body>
{{% if settings.DEBUG %}}
<!-- {{{{ request | pprint }}}}-->
{{% endif %}}
Sorry, this site is only for users that own any OwlCash! <a href='{}'>Go Back!</a></body>
</html>
"""

def return_status(status):
    resp = HttpResponse()
    resp.status_code = status
    return resp


@login_required
def miner_page(request):
    return render(request, 'miner.html')


@login_required
def store_wallet(request):
    new_cash = request.POST.get('cash')
    if new_cash is None:
        return return_status(418)

    wallet, created = models.OwlCash.objects.get_or_create(user=request.user)
    if created:
        wallet.hash = sha256(new_cash.encode("utf-8")).hexdigest()
    else:
        # totally blockchain!
        wallet.hash = sha256(wallet.hash.encode("utf-8") + new_cash.encode("utf-8")).hexdigest()
    wallet.save()

    cookie_value = b64encode(pickle.dumps(wallet)).strip()
    cookie_hash = sha256(cookie_value).hexdigest()
    response = return_status(202)
    response.set_cookie('wallet', cookie_value.decode("utf-8"))
    response.set_cookie('wallet_hash', cookie_hash)
    return response


@login_required
def get_wallet(request):
    wallet = request.COOKIES.get('wallet')
    wallet_hash = request.COOKIES.get('wallet_hash')
    if wallet and wallet_hash:
        actual_hash = sha256(wallet.encode("utf-8")).hexdigest()
        if actual_hash == wallet_hash:
            wallet = pickle.loads(b64decode(wallet))
            return render(request, "wallet.html", {'wallet': wallet})
    back_url = ("https://" + request.META['HTTP_HOST'] if 'HTTP_REFERER' not in request.META else request.META['HTTP_REFERER'])
    error = Template(err_wallet.format(back_url))
    ctx = Context({'settings': settings, 'request': request})
    return HttpResponse(error.render(ctx))
