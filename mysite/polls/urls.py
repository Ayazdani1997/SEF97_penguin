from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('create', views.createNewPoll, name='createNewPoll'),
    path('getPoll', views.getPollsById, name='getPollsById'),
    path('options', views.getOptionsOfPoll, name='getOptionsOfPoll'),
    path('vote', views.saveChoiceOfUser, name='saveChoiceOfUser'),
    path('polls', views.getPollsOfUser, name='getPollsOfUser'),
    path('emailTest', views.emailTest, name='emailTest'),
    path('finalizePoll', views.finalizePoll, name='finalizePoll'),
    path('comments/', views.getCommentsOfOption, name='getCommentsOfOption'),
    path('saveComment', views.saveCommentOfOption, name='saveComment'),
    path('result', views.checkMyPoll, name='checkMyPoll'),
    path('edit', views.editPoll, name='editPoll'),
    path('checkOverlap', views.checkOverlap, name='checkOverlap'),
    path('addoption', views.addOption, name='addOption'),
    path('addparticipants', views.addParticipants, name='addparticipants'),



]
