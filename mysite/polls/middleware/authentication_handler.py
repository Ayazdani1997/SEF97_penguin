import re

from django.http import HttpResponse, HttpResponseForbidden
from django.urls import path


class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.disallowed_urls = [re.compile(r'polls/^(login)')]

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.path in self.disallowed_urls:
            username = request.COOKIES['username']
            if username is None:
                return HttpResponseForbidden()
        return None
