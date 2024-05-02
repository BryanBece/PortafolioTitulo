from django.urls import path, include
from .views import *
from django.contrib.auth import views as auth_views
from . import views



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
    path('calendario/', calendario, name='calendario'),
    path('ver-horas-disponibles/', ver_horas_disponibles, name='ver_horas_disponibles'),
    path('reservar-hora/', reservaHora, name='reservar_hora'),
    
    
    #RegistroFono
    path('registroFono/', registroFono, name='registroFono'),
    #Comunas
    path('obtener_comunas/', obtener_comunas, name='obtener_comunas'),
    #RegistroPaciente - Tutor
    path('registroPaciente/', registroPacienteTutor, name='registroPaciente'),
    
    
    #Reset Password
    path('resetearContrasena/', resetearContrasena, name='resetearContrasena'),
    path('restablecerContrasena/<int:id>/<str:token>/', restablecerContrasena, name='restablecerContrasena'),
    
    
    

]