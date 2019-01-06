import json

from django.test import TestCase, Client
from django.urls import reverse

# Create your tests here.
from .models import *


#
# class CreatePollTest(TestCase):
#     def setUp(self):
#         self.req_params_fields = ['options', 'des', 'name']
#         self.optionListTexts = ['Tuesday', 'Thursday']
#         self.des = 'this is my poll'
#         self.name = 'my poll'
#         self.client = Client()
#
#     def testPollCreationScenario(self):
#         request_params = {self.req_params_fields[0]: self.optionListTexts, self.req_params_fields[1]: self.name,
#                           self.req_params_fields[2]: self.des}
#         response = self.client.get('polls/createPoll', request_params)
#         # rest of the code is assertion but not completed yet
#
#
# class FinalizePollTest(TestCase):
#
#     def setUp(self):
#         self.req_params_fields = ['pollId']
#         self.pollId = 1
#         self.client = Client()
#
#
#     def testPollCreationScenario(self):
#         request_params = {self.req_params_fields[0]: self.pollId}
#         self.client.get('polls/finalizePoll', request_params)
#         expectedStatus = Poll.objects.get(pollId=self.pollId)
#         self.assertEqual(expectedStatus, 1)
#
#
#
# class GetOptionsOfPollsTest(TestCase):
#     def setUp(self):
#         self.req_params_fields = ['pollId']
#         self.pollId = 1
#         self.client = Client()
#
#     def testGettingOptionsOfPoll(self):
#         request_params = {self.req_params_fields[0]: self.pollId}
#         response = self.client.get('polls/getOptions', request_params)
#         responseObject = json.loads(response.content)
#         # the rest of test is getting options from database and assert them


class RevokePollTest(TestCase):
    def setUp(self):
        testUser = User.objects.create(username="ali", email="ali@gmail.com")
        Poll.objects.create(name="Poll1", des="des of poll1", owner=testUser, status=1)
        self.client = Client()

    def test_revoke(self):
        print("working around with the tests")
        response = self.client.get(reverse('getPollsOfUser'))
        print (response.status_code)
        print(json.loads(response.content)["createdPolls"])

        response = self.client.post(reverse("finalizePoll"), data=json.dumps({"pollId": 1, "optionId":1}))
        # print("resoponse recieved")
        # print(response.status_code)
        # print(response.content)

        # self.assertEqual(lion.speak(), 'The lion says "roar"')
        # testPoll = Poll.objects.get(name="Poll1")
        # respone = self.client.get(reverse('saveChoiceOfUser'))
        # print (respone)
        # self.assertEqual(lion.speak(), 'The lion says "roar"')
        # self.assertEqual(cat.speak(), 'The cat says "meow"')
