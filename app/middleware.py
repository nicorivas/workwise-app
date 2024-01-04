import fnmatch
import logging
from itertools import chain

from django.shortcuts import redirect
from django.conf import settings


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.login_url = settings.LOGIN_URL
        self.open_urls = list(chain([self.login_url], getattr(settings, 'OPEN_URLS', [])))

    def __call__(self, request):
        logging.warning(f"MIDDLEWARE {request.path_info}")

        is_special_path = any(path in request.path_info for path in ["accounts/", "api/"])
        is_open_url = any(fnmatch.fnmatch(request.path_info, url_pattern) for url_pattern in self.open_urls)

        if not is_special_path and not request.user.is_authenticated and not is_open_url:
            return redirect(f'{self.login_url}?next={request.path}')

        return self.get_response(request)