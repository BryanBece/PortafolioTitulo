from django.urls import path, include
from .views import *
from . import views

urlpatterns = [
    # Home
    path('', home, name='home'),
    # Login
    path('login/', login, name='login'),
    # Logout
    path('logout/', logout, name='logout'),
    # Perfil
    path('perfil/', perfil, name='perfil'),
    # Equipo
    path('equipo/', equipo, name='equipo'),
    # Nosotros
    path('nosotros/', nosotros, name='nosotros'),
    # OIRS
    path('oirs/', oirs, name='oirs'),
    # Reserva
    path('calendario/', calendario, name='calendario'),
    path('ver-horas-disponibles/', ver_horas_disponibles, name='ver_horas_disponibles'),
    path('reservarHora/', reservaHora, name='reservar_hora'),
    path('cancelarReserva/<int:id>', cancelarReserva, name='cancelarReserva'),
    path('confirmarAsistencia/<int:id>', sesionAsistida, name='confirmarAsistencia'),
    path('noAsistida/<int:id>', sesionNoAsistida, name='noAsistida'),
    # RegistroFono
    path('registroFono/', registroFono, name='registroFono'),
    path('listaFonos/', listarFonos, name='listaFonos'),
    path('editarFono/<int:id>/', editarFono, name='editarFono'),
    path('eliminarFono/<int:id>/', eliminar_fono, name='eliminarFono'),
    # Comunas
    path('obtenerComunas/', obtener_comunas, name='obtener_comunas'),
    # RegistroPaciente - Tutor
    path('registroPaciente/', registroPacienteTutor, name='registroPaciente'),
    path('editarPacienteTutor/<int:id>/', editarPacienteTutor, name='editar_paciente_tutor'),
    # Reset Password
    path('resetearContrasena/', resetearContrasena, name='resetearContrasena'),
    path('restablecerContrasena/<int:id>/<str:token>/', restablecerContrasena, name='restablecerContrasena'),
    path('setPassword/<int:id>/<str:token>/', nuevaContrasenia , name='setPassword'),
    # Preguntas
    path('preguntas/', preguntas, name='preguntas'),
    path('crearPreguntas/', crearPreguntas, name='crearPreguntas'),
    path('modificarPreguntas/<int:id>', modificarPreguntas, name='modificarPreguntas'),
    path('eliminarPreguntas/<int:id>', eliminarPreguntas, name='eliminarPreguntas'),
    path('formComunicativo/<int:id>', formComunicativo, name='formComunicativo'),
    path('formSocial/<int:id>', formSocial, name='formSocial'),
    path('formLenguaje/<int:id>', formLenguaje, name='formLenguaje'),
    # Atencion
    path('busquedaPaciente/', busquedaPaciente, name='busquedaPaciente'),
    path('buscarPaciente/', views.buscar_paciente, name='buscar_paciente'),
    path('fichaClinica/<int:id>', fichaClinica, name='fichaClinica'),
    path('sesion/<int:id>', sesionFono, name='sesion'),
    path('detalleSesion/<int:id>/', detalleSesion, name='detalleSesion'),
    path('estadoOIRS/<int:solicitud_id>/', modificarOirs, name='modificarOirs'),
    path('notasPaciente/<int:id>/', notasPaciente, name='notasPaciente'),
    path('enviar/', enviarMensaje, name='enviarMensaje'),
    path('buzon/', buzonMensajes, name='buzonMensajes'),
    path('leer/<int:mensajeId>/', leerMensaje, name='leerMensaje'),
    path('responder/<int:mensajeId>/', responderMensaje, name='responderMensaje'),
    # Reportes
    path('reportes/', reportePrincipal, name='reportes'),
    path('exportar_datos/', export_data_to_excel, name='exportar_datos'),
    path('reporteReservas/', reporteReservas, name='reporteReservas'),
    path('filtrar-reservas/', filtrar_reservas, name='filtrar_reservas'),
    path('exportar-reservas-pdf/', exportar_reservas_pdf, name='exportar_reservas_pdf'),
    path('graficos/', graficos, name='graficos'),
]