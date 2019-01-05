import re

from django.http import HttpResponseForbidden, HttpResponseBadRequest

from polls.models import User


class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.disallowed_urls = [re.compile(r'^polls/(.)+')]
        self.login_url = 'polls/login'

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if any(url.match(request.path.lstrip('/')) for url in self.disallowed_urls) and not (
                request.path.lstrip('/') in self.login_url):
            try:
                username = request.COOKIES['username']
                user = User.objects.get(username=username)
                request.user = user
            except KeyError:
                return HttpResponseForbidden("forbidden page")
            except User.DoesNotExist:
                return HttpResponseBadRequest("such user not found")
        return None
