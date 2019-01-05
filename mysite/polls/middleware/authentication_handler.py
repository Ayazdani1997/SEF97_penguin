import re

from django.http import HttpResponseForbidden
from django.urls import path


class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.disallowed_urls = [re.compile(r'^polls/$')]

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if any(url.match(path) for url in self.disallowed_urls):
            username = request.COOKIES['username']
            if username is None:
                return HttpResponseForbidden()
        return None
