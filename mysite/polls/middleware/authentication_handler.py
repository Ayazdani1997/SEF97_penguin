import re

from django.http import HttpResponseForbidden, HttpResponseBadRequest

from polls.models import User


class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.disallowed_urls = [re.compile(r'^polls/(.)+')]
        self.login_api = 'login'
        self.context = 'polls/'

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if any(url.match(request.path.lstrip('/')) for url in self.disallowed_urls) and not (
                self.context + self.login_api in request.path.lstrip('/')):
            try:
                # print(request.COOKIES)
                # print(request.GET['header'])
                # username = request.COOKIES['username']
                # print("middleware")
                # print(username)
                # loggedInUser = User.objects.get(username=username)
                loggedInUser = User.objects.get(username="ali")
                request.loggedInUser = loggedInUser
            except KeyError:
                print("keyerror in middleware")
                return HttpResponseForbidden("forbidden page")
            except User.DoesNotExist:
                return HttpResponseBadRequest("such user not found")
        return None
