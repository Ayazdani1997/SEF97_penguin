import datetime
from django.db import models
from django.utils import timezone

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=200)
    uid = models.IntegerField(primary_key=True)
    email = models.EmailField(max_length=200)


class Poll(models.Model):
    pollId = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    des = models.CharField(max_length=200, default=None)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField(default=0)


class Option(models.Model):
    text = models.CharField(max_length=200)


class Choice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)


class PollOptionAssociation(models.Model):
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)


class Invitation(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


#Unnecessary Models
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)
#
#     def __str__(self):
#         return self.choice_text