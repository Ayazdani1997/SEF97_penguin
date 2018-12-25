import json

from django.test import TestCase, Client

# Create your tests here.
from polls.models import Poll


class CreatePollTest(TestCase):
    def setUp(self):
        self.req_params_fields = ['options', 'des', 'name']
        self.optionListTexts = ['Tuesday', 'Thursday']
        self.des = 'this is my poll'
        self.name = 'my poll'
        self.client = Client()

    def testPollCreationScenario(self):
        request_params = {self.req_params_fields[0]: self.optionListTexts, self.req_params_fields[1]: self.name,
                          self.req_params_fields[2]: self.des}
        response = self.client.get('polls/createPoll', request_params)
        # rest of the code is assertion but not completed yet


class FinalizePollTest(TestCase):

    def setUp(self):
        self.req_params_fields = ['pollId']
        self.pollId = 1
        self.client = Client()


    def testPollCreationScenario(self):
        request_params = {self.req_params_fields[0]: self.pollId}
        self.client.get('polls/finalizePoll', request_params)
        expectedStatus = Poll.objects.get(pollId=self.pollId)
        self.assertEqual(expectedStatus, 1)



class GetOptionsOfPollsTest(TestCase):
    def setUp(self):
        self.req_params_fields = ['pollId']
        self.pollId = 1
        self.client = Client()

    def testGettingOptionsOfPoll(self):
        request_params = {self.req_params_fields[0]: self.pollId}
        response = self.client.get('polls/getOptions', request_params)
        responseObject = json.loads(response.content)
        # the rest of test is getting options from database and assert them



