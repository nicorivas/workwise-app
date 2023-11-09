import fnmatch
import logging

from django.shortcuts import redirect
from django.conf import settings


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.login_url = settings.LOGIN_URL
        self.open_urls = [self.login_url] + getattr(settings, 'OPEN_URLS', [])

    def __call__(self, request):
        logging.warning("MIDDLEWARE "+request.path_info)
        if "accounts/" not in request.path_info:
            if not request.user.is_authenticated and \
               not any([fnmatch.fnmatch(request.path_info, l) for l in self.open_urls]):
                return redirect(self.login_url+'?next='+request.path)

        return self.get_response(request)