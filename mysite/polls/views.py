from django.db.models.query import EmptyResultSet
from django.http import HttpResponse, HttpResponseServerError
from django.core.mail import send_mail
from .models import *
import json


def notifyUser(user):
    send_mail(
        "Penguin: invitation to meeting",
        "You have been invited to a meeting in penguin please check the website for more information",
        "PenguinTeam@gmail.com",
        [user.email],
        fail_silently=False,
    )


def getOption(choice):
    return choice.pollOptionAssociation.option.text



def getLoggedInUser():
    loggedInUser = User.objects.get(username="ali")
    return loggedInUser


def getPollsOwnByUser(user):
    try:
        return [{"name":p.name, "description": p.des, "id": p.pollId} for p in list(Poll.objects.filter(owner=user))]
    except Poll.DoesNotExist:
        return []


def getInvitedPollsByUser(user):
    try:
        invitaionRecords = list(Invitation.objects.filter(user=user))
        invitedPolls = [p.poll for p in invitaionRecords]
        return [{"name": p.name, "description": p.des, "id": p.pollId} for p in invitedPolls]
    except Invitation.DoesNotExist:
        return []


# Create your views here.
def login(request):
    try:
        print("we got a login request")
        username = request.GET['username']
        email = request.GET['email']
        print ("before DB")
        loggedInUser = User.objects.get(username=username, email=email)
        print("after DB")
    except User.DoesNotExist:
        print ("User does not exist exception in login")
        return HttpResponse(loggedInUser)
    except KeyError:
        print("arg not provided")
        loggedInUser = getLoggedInUser()
        loggedInUser = {"username": loggedInUser.username, "email": loggedInUser.email}
        return HttpResponse(json.dumps(loggedInUser))
    else:
        print("okay in logins")
        response = {"username" : loggedInUser.username , "email": loggedInUser.email}
        json_respone = json.dumps(response)
        print(json_respone)
        return HttpResponse(json_respone)
        # return HttpResponse("the DB has fucked us")



def createNewPoll(request):
    user = getLoggedInUser()
    try:
        pollName = request.GET['name']
        pollDes = request.GET['des']
        newPoll = Poll.objects.create(name=pollName, des=pollDes, owner=user)
        optionsTexts = request.GET['options']
        for optionText in optionsTexts:
            try:
                newOption = Option.objects.get(text=optionText)
            except Option.DoesNotExist:
                newOption = Option.objects.create(text=optionsTexts)
            PollOptionAssociation.objects.create(poll=newPoll, option=newOption)
        invitedUserIds= request.GET['invitedList']
        for userId in invitedUserIds:
            targetUser = User.objects.get(uid=userId)
            notifyUser(targetUser)
            Invitation.objects.create(poll=newPoll, user=targetUser)


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
        data = {}
        data['pollId'] = requestedPoll.pollId
        jsonPoll = json.dumps(data)
        return HttpResponse(jsonPoll)


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
    print("getPollsOfUser")
    user = getLoggedInUser()
    response = {}
    response['createdPolls'] = getPollsOwnByUser(user)
    response["invitedPolls"] = getInvitedPollsByUser(user)

    print(response)
    jsonResponse = json.dumps(response)
    return HttpResponse(jsonResponse)


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
            pollOptionAssociations = list(PollOptionAssociation.objects.filter(poll=targetPoll))
            finalResponse = []

            for POA in pollOptionAssociations:
                option = POA.option
                optionChoice = {"id" : option.id, "text": option.text}
                print(optionChoice)

                choices = (list(Choice.objects.filter(pollOptionAssociation=POA)))
                selectors = []
                rejectors = []
                maybe = []
                for c in choices:
                        print(c.user.username)
                        print(c.answer)
                        if (c.answer ==1):
                            selectors.append(c.user.username)
                        elif (c.answer == 2):
                            rejectors.append(c.user.username)
                        elif (c.answer == 3):
                            maybe.append(c.user.username)

                optionChoice["selectors"] = selectors
                optionChoice["rejectors"] = rejectors
                optionChoice["maybe"] = maybe
                finalResponse.append(optionChoice)

            jsonResponse = json.dumps(finalResponse)
            return HttpResponse(jsonResponse)
        except PollOptionAssociation.DoesNotExist:
            return HttpResponse("POA doesn't exist")
        except Choice.DoesNotExist:
            return HttpResponse("Choice doesnt exist")
        except User.DoesNotExist:
            return HttpResponseServerError("internal server error")


def emailTest(request):
    user = getLoggedInUser()
    notifyUser(user)
    return HttpResponse("successfully sent email to %s" % user.email)
