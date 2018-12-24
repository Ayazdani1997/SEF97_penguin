from django.db.models.query import EmptyResultSet
from django.http import HttpResponse, HttpResponseServerError
from polls.models import *


def getLoggedInUser():
    loggedInUser = User.objects.get(username="ahmad")
    return loggedInUser


# Create your views here.
def login(request):
    try:
        username = request.GET['username']
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
        return HttpResponseServerError("internal server error")
    else:
        return HttpResponse("poll %s created successfully" % Poll.objects.get(name=pollName).des)


def getPollsById(request):
    try:
        pollId = request.GET['pollId']
        requestedPoll = Poll.objects.get(pollId=pollId)

    except Poll.DoesNotExist:
        return HttpResponse("requested poll does not exist in system!")
    else:
        return HttpResponse(requestedPoll)


def getOptionsOfPoll(request):
    try:
        pollId = request.GET['pollId']
        requestedPoll = Poll.objects.get(pollId=pollId)
        print( PollOptionAssociation.objects.get(poll=requestedPoll ) )
    except Poll.DoesNotExist:
        return HttpResponse("requested poll does not exist in system!")
    except EmptyResultSet:
        return HttpResponse("this poll does not have any options!")
    else:
        return requestedPoll




def saveChoiceOfUser(request):
    global optionText
    try:
        pollId = request.content_params['pollId']
        optionText = request.content_params['optionText']
        poll = Poll.objects.get(pollId=pollId)
        option = Option.objects.get(text=optionText)
        user = getLoggedInUser()
        Choice.objects.create(user=user, option=option, poll=poll)
        # return HttpResponse( "your choice saved" )
    except Poll.DoesNotExist:
        return HttpResponse("requested poll does not exist in system!")
    except Option.DoesNotExist:
        return HttpResponse("option %s does not exist in this poll" % optionText)
    except PollOptionAssociation:
        return HttpResponse("option %s does not exist in this poll" % optionText)
    except KeyError:
        return HttpResponseServerError("internal server error")
    else :
        return HttpResponse( "choices saved" );
