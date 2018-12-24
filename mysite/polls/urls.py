from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('createPoll', views.createNewPoll, name='createNewPoll'),
    path('getPoll', views.getPollsById, name='getPollsById'),
    path('getOptions', views.getOptionsOfPoll, name='getOptionsOfPoll'),
    path('saveChoice', views.saveChoiceOfUser, name='saveChoiceOfUser'),
    path('polls', views.getPollsOfUser , name='getPollsOfUser'),
    path('emailTest', views.emailTest, name='emailTest'),
    path('finalizePoll', views.finalizePoll, name='finalizePoll'),

]
