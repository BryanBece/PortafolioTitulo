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
    path('cancelarReserva/<int:id>', cancelarReserva, name='cancelarReserva'),
    path('confirmarAsistencia/<int:id>', sesionAsistida, name='confirmarAsistencia'),
    path('noAsistida/<int:id>', sesionNoAsistida, name='noAsistida'),
    
    
    #RegistroFono
    path('registroFono/', registroFono, name='registroFono'),
    path('listaFonos/', listarFonos, name='listaFonos'),
    path('editarFono/<int:id>/', editarFono, name='editarFono'),
    path('eliminarFono/<int:id>/', eliminar_fono, name='eliminarFono'),
    #Comunas
    path('obtener_comunas/', obtener_comunas, name='obtener_comunas'),
    #RegistroPaciente - Tutor
    path('registroPaciente/', registroPacienteTutor, name='registroPaciente'),
    path('editar_paciente_tutor/<int:id>/', editarPacienteTutor, name='editar_paciente_tutor'),
    
    
    #Reset Password
    path('resetearContrasena/', resetearContrasena, name='resetearContrasena'),
    path('restablecerContrasena/<int:id>/<str:token>/', restablecerContrasena, name='restablecerContrasena'),
    path('setPassword/<int:id>/<str:token>/', nuevaContrasenia , name='setPassword'),

    #Preguntas
    path('preguntas/', preguntas, name='preguntas'),
    path('crearPreguntas/', crearPreguntas, name='crearPreguntas'),
    path('modificarPreguntas/<int:id>', modificarPreguntas, name='modificarPreguntas'),
    path('eliminarPreguntas/<int:id>', eliminarPreguntas, name='eliminarPreguntas'),
    
    
    #Atencion
    path('busquedaPaciente/', busquedaPaciente, name='busquedaPaciente'),
    path('buscar_paciente/', views.buscar_paciente, name='buscar_paciente'),
    path('fichaClinica/<int:id>', fichaClinica, name='fichaClinica'),
    path('sesion/<int:id>', sesionFono, name='sesion'),
    path('detalleSesion/<int:id>/', detalleSesion, name='detalleSesion'),
    
    #Reportes
    path('reportes/', reportePrincipal, name='reportes'),
    path('exportar-datos/', export_data_to_excel, name='exportar_datos'),
    path('reporteReservas/', reporteReservas, name='reporteReservas'),
    path('filtrar-reservas/', filtrar_reservas, name='filtrar_reservas'),
    path('exportar-reservas-pdf/', exportar_reservas_pdf, name='exportar_reservas_pdf'),
    

]