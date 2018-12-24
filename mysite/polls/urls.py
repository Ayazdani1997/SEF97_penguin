from django.urls import path
from . import views

urlpatterns = [
        path('', views.index, name='index'),
        path('login', views.login, name='login'),
        path( 'createPoll' , views.createNewPoll , name='createNewPoll' ),
        path( 'getPoll' , views.getPollsById , name='getPollsById' )
]
