from django.urls import path, include
from .views import *
from .import views



urlpatterns = [
    #Home
    path('', home, name='home'),
    #Login
    path('login/', login, name='login'),
    #Logout
    path('logout/', logout, name='logout'),
    #Perfil
    path('perfil/', perfil, name='perfil'),
    #Equipo
    path('equipo/', equipo, name='equipo'),
    #Nosotros
    path('nosotros/', nosotros, name='nosotros'),
    #OIRS
    path('oirs/', oirs, name='oirs'),
    #Reserva
    path('reserva/', reserva, name='reserva'),
]