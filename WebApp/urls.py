from django.urls import path, include
from .views import *
from .import views



urlpatterns = [
    #Home
    path('', home, name='home'),
]