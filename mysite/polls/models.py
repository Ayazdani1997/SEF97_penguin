from django.db import models


# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=200)
    uid = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=200)
    def getByUserName(self , username ) :
        return self.objects.get( username = username)

class Poll(models.Model):
    pollId = models.AutoField(primary_key=True)
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
    pollOptionAssociation = models.ForeignKey(PollOptionAssociation, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
