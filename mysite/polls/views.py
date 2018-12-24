from django.http import HttpResponse
from polls.models import *


#
def getLoggedInUser():
    # loggedInUser = userInstance.getByUserName(username)
    loggedInUser = User.objects.get(username="ahmad")
    return loggedInUser


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


# Create your views here.
def login(request):
    try:
        username = request.GET['username']
        email = request.GET['email']
        loggedInUser = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse("this user does not exist in system")
    else:
        return HttpResponse(loggedInUser)


def createNewPoll(request):
    user = getLoggedInUser()
    try:
        pollName = request.GET['name']
        pollDes = request.GET['des']
        Poll.objects.create(name=pollName, des=pollDes, owner=user)
    except KeyError:
        return HttpResponse("cannot create poll")
    else:
        return HttpResponse("poll %s created successfully" % Poll.objects.get(name=pollName).des)


def getPollsById(request):
    try:
        pollId = request.GET['pollId']
        requestedPoll = Poll.objects.get(pollId=pollId)

    except User.DoesNotExist:
        return HttpResponse("requested poll does not exist in system")
    else:
        return HttpResponse(requestedPoll)
