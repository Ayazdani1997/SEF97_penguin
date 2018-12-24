from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('createPoll', views.createNewPoll, name='createNewPoll'),
    path('getPoll', views.getPollsById, name='getPollsById'),
    path('getOptions', views.getOptionsOfPoll, name='getOptionsOfPoll'),
    path('saveChoice', views.saveChoiceOfUser, name='saveChoiceOfUser')
]
