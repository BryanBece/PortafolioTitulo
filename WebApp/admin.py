from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['id', 'region']
    search_fields = ['region']
    
@admin.register(Comuna)
class ComunaAdmin(admin.ModelAdmin):
    list_display = ['id','comuna', 'region']
    search_fields = ['comuna', 'region']
    
@admin.register(Clinica)
class ClinicaAdmin(admin.ModelAdmin):
    list_display = ['id','nombre', 'direccion', 'comuna']
    search_fields = ['nombre', 'direccion', 'comuna']

@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    list_display = ['id','genero']
    search_fields = ['genero']
    
@admin.register(Fonoaudiologo)
class FonoaudiologoAdmin(admin.ModelAdmin):
    list_display = ['id','nombre', 'apellido', 'rut', 'genero', 'telefono', 'email', 'clinica']
    search_fields = ['nombre', 'apellido', 'rut', 'genero', 'telefono', 'email', 'clinica']
    
@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ['id','nombre', 'apellido', 'rut', 'fechaNacimiento', 'genero', 'telefono', 'direccion', 'comuna', 'tutor']
    search_fields = ['rut']
    
@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ['id','nombreTutor', 'apellidoTutor', 'rutTutor', 'generoTutor', 'telefonoTutor', 'emailTutor']
    search_fields = ['nombreTutor', 'apellidoTutor', 'rutTutor', 'generoTutor', 'telefonoTutor', 'emailTutor']
    
@admin.register(HorasTrabajo)
class HorasTrabajoAdmin(admin.ModelAdmin):
    list_display = ['doctor','dia_semana', 'hora_inicio', 'hora_fin']
    search_fields = ['dia_semana', 'fonoaudiologo']
    
@admin.register(ReservaHora)
class ReservaHoraAdmin(admin.ModelAdmin):
    list_display = ['id','fecha', 'hora', 'fonoaudiologo', 'nombrePaciente', 'apellidoPaciente', 'rutPaciente','telefonoPaciente','emailPaciente','estado']
    search_fields = ['fecha', 'fonoaudiologo', 'paciente','estado']
    
@admin.register(SesionTerapeutica)
class SesionTerapeuticaAdmin(admin.ModelAdmin):
    list_display = ['id','fecha', 'actividades', 'tareas', 'fonoaudiologo', 'paciente', 'tutor']
    search_fields = ['fecha', 'fonoaudiologo', 'paciente']
    
@admin.register(Formulario)
class FormularioAdmin(admin.ModelAdmin):
    list_display = ['id','nombre', 'numero']
    search_fields = ['nombre', 'numero']
    
@admin.register(PreguntaFormulario)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = ['id','textoPregunta', 'formulario']
    search_fields = [ 'formulario']
    
@admin.register(RespuestaFormulario)
class RespuestaAdmin(admin.ModelAdmin):
    list_display = ['id','respuesta', 'pregunta', 'paciente','fechaRespuesta']
    search_fields = ['respuesta', 'pregunta', 'paciente']
    
@admin.register(OIRS)
class OIRSAdmin(admin.ModelAdmin):
    list_display = ('tipo_mensaje', 'nombre', 'email', 'telefono','estado', 'mensaje','fecha_creacion')
    list_filter = ('tipo_mensaje', 'fecha_creacion','estado')
    search_fields = ('nombre', 'email', 'mensaje', 'telefono','estado')
    
@admin.register(Mensaje)
class MensajeAdmin(admin.ModelAdmin):
    list_display = ('id','emisor', 'receptor', 'paciente','texto','fechaEnvio','leidoUno','leidoDos')