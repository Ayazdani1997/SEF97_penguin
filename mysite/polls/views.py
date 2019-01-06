from django.db.models.query import EmptyResultSet
from django.http import HttpResponse, HttpResponseServerError, HttpResponseBadRequest, HttpResponseForbidden, \
    HttpResponseNotFound
from django.core.mail import send_mail
from django.utils.datastructures import MultiValueDictKeyError

import datetime
from .models import *
from django.views.decorators.csrf import csrf_exempt

import json


def notifyUser(user, message="You have new notification in penguin please check the website for more information"):
    print("notifyUser")
    print(message)
    send_mail(
        "Penguin: invitation to meeting",
        message,
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
        return [{"name": p.name, "description": p.des, "id": p.pollId} for p in list(Poll.objects.filter(owner=user))]
    except Poll.DoesNotExist:
        return []


def getInvitedPollsByUser(user):
    try:
        invitaionRecords = list(Invitation.objects.filter(user=user))
        invitedPolls = [p.poll for p in invitaionRecords]
        return [{"status": p.status, "name": p.name, "description": p.des, "id": p.pollId} for p in invitedPolls]
    except Invitation.DoesNotExist:
        return []


def isInvitedToPollOrOwner(user, poll):
    try:
        invitation = Invitation.objects.get(user=user, poll=poll)
        return True
    except Invitation.DoesNotExist:
        if user == poll.owner:
            return True
        return False


# Create your views here.
def login(request):
    try:
        print("we got a login request")
        username = request.GET['username']
        email = request.GET['email']
        print("before DB")
        loggedInUser = User.objects.get(username=username, email=email)
    except MultiValueDictKeyError:
        return HttpResponseBadRequest("no or more than one user specified on login request")
    except User.DoesNotExist:
        print("User does not exist exception in login")
        return HttpResponseNotFound("the user does not exists in system")
    except KeyError:
        print("arg not provided")
        loggedInUser = getLoggedInUser()
        loggedInUser = {"username": loggedInUser.username, "email": loggedInUser.email}
        return HttpResponse(json.dumps(loggedInUser))
    else:
        userInfo = {'username': username, "email": email}
        response = HttpResponse(json.dumps(userInfo))
        response.set_cookie('username', username)
        return response

@csrf_exempt
def createNewPoll(request):
    print("createpoll")
    user = request.loggedInUser
    print(user)
    try:
        body = json.loads(request.body)['body']
        print(body)
        pollName = body['name']
        if (body["periodic"]):
            pollName = "Periodic Poll -- " + pollName
        pollDes = body['description']
        newPoll = Poll.objects.create(name=pollName, des=pollDes, owner=user)
        newPoll.save()

    except KeyError:
        return HttpResponseServerError("internal server error")
    else:
        return HttpResponse(json.dumps({'pollId': newPoll.pollId}))

@csrf_exempt
def addOption(request):
    body = json.loads(request.body)['body']
    print(body)
    newPoll = Poll.objects.get(pollId=body['id'])
    optionsTexts = body['options']
    for optionText in optionsTexts:
        try:
            isPeriodic = body["periodic"]
            startTimeText = optionText
            if isPeriodic:
                startTimeText = optionText.split(",")[0]
            optionDateTime = datetime.datetime.strptime(startTimeText, "%Y-%m-%d %H:%M")
            newOption = Option.objects.get(start=optionDateTime, text=optionText)
            print("we already have the option")

        except Option.DoesNotExist:
            print("option does not exist")
            newOption = Option.objects.create(start=optionDateTime, text=optionText)
            newOption.save()
            print("created option")
        newPollOptAss = PollOptionAssociation.objects.create(poll=newPoll, option=newOption)
        newPollOptAss.save()
        print("created poll option ass new")


def getOptionById(request):
    try:
        print("getOptionById")
        optionId = request.GET["optionId"]
        print(optionId)
        targetOption = Option.objects.get(OptionId=optionId)
        print(targetOption.start)
        print(targetOption.text)
    except Option.DoesNotExist:
        print("option does not exist")

    return HttpResponse(json.dumps({"text": targetOption.text}))

def createPeriodicMessage(times):
    print("createPeriodicPoll")
    msg = ""
    start = times[0]
    end = times[1]
    period = int(times[2])
    startdate = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M")
    enddate = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M")
    while(startdate +datetime.timedelta(days=period) < enddate):
        msg = msg + startdate.strftime("%Y-%m-%d %H:%M") + "\n"
        startdate = startdate +datetime.timedelta(days=period)

    return msg

@csrf_exempt
def addParticipants(request):
    body = json.loads(request.body)['body']
    print(body)
    newPoll = Poll.objects.get(pollId=body['id'])
    invitedUserEmails= body['participants']
    isPeriodic = body["periodic"]
    msg = "you have new poll invitation, please check the penguin website"
    if isPeriodic:
        msg = msg+ "\n the poll is periodic!"
        pollOpAsses = list(PollOptionAssociation.objects.filter(poll=newPoll))
        for pollOpAss in pollOpAsses:
            option = pollOpAss.option
            msg = msg + "\n-----------------\n"
            times = option.text.split(",")
            print(times)
            msg = msg + createPeriodicMessage(times)

    print(msg)
    for email in invitedUserEmails:
        targetUser = User.objects.get(email=email)
        print(targetUser)
        notifyUser(targetUser, msg)
        newInvitation = Invitation.objects.create(poll=newPoll, user=targetUser)
        newInvitation.save()



def getPollsById(request):
    try:
        pollId = request.GET['pollId']
        requestedPoll = Poll.objects.get(pollId=pollId)

    except Poll.DoesNotExist:
        return HttpResponse("requested poll does not exist in system!")
    else:
        data = {'pollId': requestedPoll.pollId}
        jsonPoll = json.dumps(data)
        return HttpResponse(jsonPoll)





def getOptionsOfPoll(request):
    try:
        pollId = request.GET['pollId']
        requestedPoll = Poll.objects.get(pollId=pollId)
        option_associations = PollOptionAssociation.objects.filter(poll=requestedPoll)
        response = []
        for option_association in option_associations:
            option = option_association.option
            new_response = {"id": option.OptionId, "text": option.text}
            response.append(new_response)
    except Poll.DoesNotExist:
        return HttpResponse("requested poll does not exist in system!")
    except EmptyResultSet:
        return HttpResponse("this poll does not have any options!")
    else:

        return HttpResponse(json.dumps(response))


@csrf_exempt
def saveChoiceOfUser(request):
    print("saveChoiceOfUser")
    try:
        body = json.loads(request.body)['body']
        pollId = body["pollId"]
        print(pollId)
        choices = body['choices']
        print(choices)
        poll = Poll.objects.get(pollId=pollId)
        user = request.loggedInUser
        for choice in choices:
            print(choice['optionId'])
            print(choice['answer'])
            targetOption = Option.objects.get(OptionId=choice['optionId'])
            pollOptionAssociation = PollOptionAssociation.objects.get(poll=poll, option=targetOption)
            try:
                newChoice = Choice.objects.get(user= user , pollOptionAssociation=pollOptionAssociation)
                newChoice.answer = choice['answer']
                newChoice.save()
            except Choice.DoesNotExist:
                newChoice = Choice.objects.create(user=user, pollOptionAssociation=pollOptionAssociation,
                                                  answer=choice['answer'])
                newChoice.save()

    except PollOptionAssociation.DoesNotExist:
        return HttpResponse("requested polloptassociation does not exist in system!")
    except Option.DoesNotExist:
        return HttpResponse("option %s does not exist in this poll")
    except PollOptionAssociation.DoesNotExist:
        return HttpResponse("option %s does not exist in this poll")
    except KeyError:
        return HttpResponseServerError("internal server error")
    else:
        response = checkOverlap(user)
        return HttpResponse(json.dumps(response))


def checkOverlap(user):
    print("checkOverlap")
    choices = list(Choice.objects.filter(user=user, answer=1))
    print(choices)
    finalizedOptions = []
    for choice in choices:
        pollStatus = choice.pollOptionAssociation.poll.status
        if pollStatus:
            finalizedOptions.append({"option": Option.objects.get(OptionId=pollStatus), "choice": choice})
    options = [{"option": choice.pollOptionAssociation.option, "choice": choice} for choice in choices]
    print(finalizedOptions)
    print(options)
    for elem1 in options:
        overlap = False
        for elem2 in finalizedOptions:
            if (elem1["option"].start == elem2["option"].start and elem1!=elem2):
                overlap = True
        if overlap:
            overlapMessage = "overlap detected between" + elem1["choice"].pollOptionAssociation.poll.name + " and " + elem2["choice"].pollOptionAssociation.poll.name
            print(overlapMessage)
            return({"overlap":True, "overlapMessage": overlapMessage})
    return({"overlap":False, "overlapMessage": ""})


def checkOverlapTest(request):
    user = request.loggedInUser
    checkOverlap(user)
    return HttpResponse("test done")

@csrf_exempt
def editPoll(request):
    print('editpoll')
    body = json.loads(request.body)['body']
    pollId = body['pollId']
    poll = Poll.objects.get(pollId=pollId)
    print(body)
    for key in body.keys():
        if (key == "newOption"):
            newOption = Option.objects.create(text=body[key])
            newOption.save()
        elif key=="name":
            poll.name = body[key]
        elif key == "des":
            poll.des = body[key]
    poll.save()

    return HttpResponse("editpoll")



def getPollsOfUser(request):
    user = request.loggedInUser
    response = {'createdPolls': getPollsOwnByUser(user), "invitedPolls": getInvitedPollsByUser(user)}

    print(response)
    jsonResponse = json.dumps(response)
    return HttpResponse(jsonResponse)

@csrf_exempt
def finalizePoll(request):
    user = request.loggedInUser
    body = json.loads(request.body)['body']
    targetPoll = Poll.objects.get(pollId=body['pollId'])
    targetOption = Option.objects.get(OptionId=body['optionId'])
    if user != targetPoll.owner:
        return HttpResponse("you are not authorized to finalize this poll")
    else:
        targetPoll.status = body['optionId']
        targetPoll.save()
        return HttpResponse(" successfully finialized poll %s" % targetPoll.name)


@csrf_exempt
def revokePoll(request):
    user = request.loggedInUser
    body = json.loads(request.body)['body']
    targetPoll = Poll.objects.get(pollId=body['pollId'])
    if user != targetPoll.owner:
        return HttpResponse("you are not authorized to revoke this poll")
    else:
        targetPoll.status = 0
        targetPoll.save()
        invitationList = list(Invitation.objects.filter(poll=targetPoll))
        revokeMsg = body['msg']
        for invitation in invitationList:
            notifyUser(invitation.user, revokeMsg)
        return HttpResponse(" Poll has been revoked and participants have been notified! %s" % targetPoll.name)



def checkMyPoll(request):
    user = request.loggedInUser
    targetPoll = Poll.objects.get(pollId=request.GET['pollId'])
    if user != targetPoll.owner:
        return HttpResponse("you are not authorized to check the status of this poll")
    else:
        try:
            pollOptionAssociations = list(PollOptionAssociation.objects.filter(poll=targetPoll))
            optionChoiceList = []

            for POA in pollOptionAssociations:
                option = POA.option
                optionChoice = {"id" : option.OptionId, "text": option.text}
                print(optionChoice)

                choices = (list(Choice.objects.filter(pollOptionAssociation=POA)))
                selectors = []
                rejectors = []
                maybe = []
                for c in choices:
                        print(c.user.username)
                        print(c.answer)
                        if (c.answer ==1):
                            selectors.append({"name": c.user.username})
                        elif (c.answer == 2):
                            rejectors.append({"name": c.user.username})
                        elif (c.answer == 3):
                            maybe.append({"name": c.user.username})

                optionChoice["selectors"] = selectors
                optionChoice["rejectors"] = rejectors
                optionChoice["maybe"] = maybe
                optionChoiceList.append(optionChoice)
            finalResponse = {"status": targetPoll.status, "optionChoiceList": optionChoiceList}
            jsonResponse = json.dumps(finalResponse)
            return HttpResponse(jsonResponse)
        except PollOptionAssociation.DoesNotExist:
            return HttpResponse("POA doesn't exist")
        except Choice.DoesNotExist:
            return HttpResponse("Choice doesnt exist")
        except User.DoesNotExist:
            return HttpResponseServerError("internal server error")


def getCommentsOfOption(request):
    try:
        print(request.GET)
        pollId = request.GET['pollId']
        optionId = request.GET['optionId']
        print(pollId)
        print(optionId)
    except KeyError:
        return HttpResponseBadRequest("no poll or option identified")
    option = Option.objects.get(OptionId=optionId)
    poll = Poll.objects.get(pollId=pollId)
    if not isInvitedToPollOrOwner(request.loggedInUser, poll):
        return HttpResponseForbidden('you are not invited to this poll')
    pollOptionAssociation = PollOptionAssociation.objects.get(poll=poll, option=option)
    comments = Comment.objects.filter(pollOptionAssociation=pollOptionAssociation).values_list('comment_text',
                                                                                               'owner__username')
    response_data = {'comments': [{'text': comment[0], 'user': comment[1]} for comment in comments]}
    response = HttpResponse(json.dumps(response_data))
    return response


@csrf_exempt
def saveCommentOfOption(request):
    try:
        body = json.loads(request.body)['body']
        print(body)
        pollId = body['pollId']
        print(pollId)
        optionId = body['optionId']
        print(optionId)
        comment_text = body['comment_text']
        print(comment_text)
    except KeyError:
        return HttpResponseBadRequest("no poll or option identified, plus, comment must have a text")
    option = Option.objects.get(OptionId=optionId)
    poll = Poll.objects.get(pollId=pollId)
    if not isInvitedToPollOrOwner(request.loggedInUser, poll):
        return HttpResponseForbidden('you are not invited to this poll')
    pollOptionAssociation = PollOptionAssociation.objects.get(poll=poll, option=option)
    comment = Comment.objects.create(pollOptionAssociation=pollOptionAssociation, comment_text=comment_text,
                           owner=request.loggedInUser)
    comment.save()
    return HttpResponse()


def emailTest(request):
    user = request.loggedInUser
    notifyUser(user)
    return HttpResponse("successfully sent email to %s" % user.email)
