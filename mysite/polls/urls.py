from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('createPoll', views.createNewPoll, name='createNewPoll'),
    path('getPoll', views.getPollsById, name='getPollsById'),
    path('options', views.getOptionsOfPoll, name='getOptionsOfPoll'),
    path('vote', views.saveChoiceOfUser, name='saveChoiceOfUser'),
    path('polls', views.getPollsOfUser, name='getPollsOfUser'),
    path('emailTest', views.emailTest, name='emailTest'),
    path('finalizePoll', views.finalizePoll, name='finalizePoll'),
    path('result', views.checkMyPoll, name='checkMyPoll'),
    path('edit', views.editPoll, name='editPoll'),

]
