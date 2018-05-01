import time
from django.conf import settings
from django.utils.cache import patch_vary_headers
from django.urls import set_urlconf


class MultiHostMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)
        response = self.get_response(request)
        return self.process_response(request, response)

    def process_request(self, request):
        try:
            request.META["LoadingStart"] = time.time()
            host = request.META["HTTP_HOST"]
            host_port = host.split(':')
            if len(host_port) == 2:
                host = host_port[0] 
            sub_dom = host.split('.')[0]
            if sub_dom in list(settings.HOST_MIDDLEWARE_URLCONF_MAP.keys()):
                new_url_conf = settings.HOST_MIDDLEWARE_URLCONF_MAP[sub_dom]
                set_urlconf(new_url_conf)
                request.urlconf = new_url_conf
                request.META["MultiHost"] = new_url_conf
            else:
                request.META["MultiHost"] = str(settings.ROOT_URLCONF)

        except KeyError:
            pass  # use default urlconf (settings.ROOT_URLCONF)

    def process_response(self, request, response):
        if 'MultiHost' in request.META:
            response['MultiHost'] = request.META.get("MultiHost")

        if 'LoadingStart' in request.META:
            _loading_time = time.time() - int(request.META["LoadingStart"])
            response['LoadingTime'] = "%.2fs" % (_loading_time, )

        if getattr(request, "urlconf", None):
            patch_vary_headers(response, ('Host',))
        return response
