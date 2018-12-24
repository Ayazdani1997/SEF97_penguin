from django.db.models.query import EmptyResultSet
from django.http import HttpResponse, HttpResponseServerError
from django.core.mail import send_mail
from .models import *


def notifyUser(user):
    send_mail(
        "Penguin: invitation to meeting",
        "You have been invited to a meeting in penguin please check the website for more information",
        "PenguinTeam@gmail.com",
        [user.email],
        fail_silently=False,
    )


def getLoggedInUser():
    loggedInUser = User.objects.get(username="ahmad")
    return loggedInUser


def getPollsOwnByUser(user):
    try:
        return list(Poll.objects.filter(owner=user))
    except Poll.DoesNotExist:
        return []


def getInvitedPollsByUser(user):
    try:
        invitaionRecords = list(Invitation.objects.filter(user=user))
        return [p.poll for p in invitaionRecords]

    except Invitation.DoesNotExist:
        return []


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
        option = PollOptionAssociation.objects.get(poll=requestedPoll).option
    except Poll.DoesNotExist:
        return HttpResponse("requested poll does not exist in system!")
    except EmptyResultSet:
        return HttpResponse("this poll does not have any options!")
    else:
        return HttpResponse(option)


def saveChoiceOfUser(request):
    global optionText
    try:
        pollId = request.GET['pollId']
        optionText = request.GET['optionText']
        poll = Poll.objects.get(pollId=pollId)
        option = Option.objects.get(text=optionText)
        user = getLoggedInUser()
        Choice.objects.create(user=user, option=option)
    except Poll.DoesNotExist:
        return HttpResponse("requested poll does not exist in system!")
    except Option.DoesNotExist:
        return HttpResponse("option %s does not exist in this poll" % optionText)
    except PollOptionAssociation.DoesNotExist:
        return HttpResponse("option %s does not exist in this poll" % optionText)
    except KeyError:
        return HttpResponseServerError("internal server error")
    else:
        return HttpResponse("choices saved")


def getPollsOfUser(request):
    user = getLoggedInUser()
    response = {"createdPolls": getPollsOwnByUser(user), "invitedPolls": getInvitedPollsByUser(user)}

    print(response)
    return HttpResponse(response)


def finalizePoll(request):
    user = getLoggedInUser()
    targetPoll = Poll.objects.get(pollId=request.GET['pollId'])
    if user != targetPoll.owner:
        return HttpResponse("you are not authorized to finalize this poll")
    else:
        targetPoll.status = 1
        targetPoll.save()
        return HttpResponse(" successfully finialized poll %s" % targetPoll.name)


def checkMyPoll(request):
    user = getLoggedInUser()
    targetPoll = Poll.objects.get(pollId=request.GET['pollId'])
    if user != targetPoll.owner:
        return HttpResponse("you are not authorized to check the status of this poll")
    else:
        try:
            pollOptionAssociations = PollOptionAssociation.objects.get(poll=targetPoll)
            participants = list(pollOptionAssociations.choice_set().value_list('user', flat=True))
            return HttpResponse(participants)
        except Choice.DoesNotExist:
            return HttpResponse([])
        except User.DoesNotExist:
            return HttpResponseServerError( "internal server error" )


def emailTest(request):
    user = getLoggedInUser()
    notifyUser(user)
    return HttpResponse("successfully sent email to %s" % user.email)
