from django.db import models


# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=200)
    uid = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=200)


class Poll(models.Model):
    pollId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    des = models.CharField(max_length=200, default=None)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField(default=0)


class Option(models.Model):
    text = models.CharField(max_length=200)
    start = models.DateTimeField(auto_now=True)
    end = models.DateTimeField(auto_now=True)
    OptionId = models.AutoField(primary_key=True)


class PollOptionAssociation(models.Model):
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)


class Choice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pollOptionAssociation = models.ForeignKey(PollOptionAssociation, on_delete=models.CASCADE, null=False)
    answer = models.IntegerField(default=0)  # enum - choices


class Invitation(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model):
    commentId = models.AutoField(primary_key=True)
    comment_text = models.CharField(max_length=200, default=None)
    pollOptionAssociation = models.ForeignKey(PollOptionAssociation, on_delete=models.CASCADE, null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

