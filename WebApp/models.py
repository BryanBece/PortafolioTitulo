from django.db import models
from user.models import User
from django.utils import timezone

# Create your models here.

#Region
class Region(models.Model):
    id = models.AutoField(primary_key=True)
    region = models.CharField(max_length=100)
    
    def __str__(self):
        return self.region
    
#Comuna
class Comuna(models.Model):
    id = models.AutoField(primary_key=True)
    comuna = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.comuna} - {self.region.region}'
    
#Clinica
class Clinica(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre
    
#Genero
class Genero(models.Model):
    id = models.AutoField(primary_key=True)
    genero = models.CharField(max_length=100)
    
    def __str__(self):
        return self.genero
    
#Fonoaudiologo
class Fonoaudiologo(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    rut = models.CharField(max_length=10)
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=9)
    email = models.EmailField(max_length=100)
    clinica = models.ForeignKey(Clinica, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.nombre} {self.apellido}'
    
#Tutor
class Tutor(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    rut = models.CharField(max_length=12)
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=9)
    email = models.EmailField(max_length=100, unique=True)
    
    def __str__(self):
        return f'{self.nombre} {self.apellido}'
    
#Paciente
class Paciente(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    rut = models.CharField(max_length=12)
    fechaNacimiento = models.DateField(default=timezone.now)
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=9)
    direccion = models.CharField(max_length=100)
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.nombre} {self.apellido}'
    

#Reserva Hora
class ReservaHora(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateField(default=timezone.now)
    hora = models.TimeField()
    fonoaudiologo = models.ForeignKey(Fonoaudiologo, on_delete=models.CASCADE)
    nombrePaciente = models.CharField(max_length=100)
    apellidoPaciente = models.CharField(max_length=100)
    rutPaciente = models.CharField(max_length=12)
    telefonoPaciente = models.CharField(max_length=9)
    emailPaciente = models.EmailField(max_length=100)
    estado = models.CharField(max_length=10, default='Reservada')
    
    def __str__(self):
        return f'{self.nombrePaciente} - {self.apellidoPaciente} -{self.fonoaudiologo} - {self.fecha} - {self.hora}'
    
#Horario Fonoaudiologos
class HorasTrabajo(models.Model):
    LUNES = 0
    MARTES = 1
    MIERCOLES = 2
    JUEVES = 3
    VIERNES = 4

    DIA_CHOICES = [
        (LUNES, 'Lunes'),
        (MARTES, 'Martes'),
        (MIERCOLES, 'Miércoles'),
        (JUEVES, 'Jueves'),
        (VIERNES, 'Viernes'),
    ]

    doctor = models.ForeignKey(Fonoaudiologo, related_name='horas_trabajo', on_delete=models.CASCADE)
    dia_semana = models.IntegerField(choices=DIA_CHOICES, default=LUNES)
    hora_inicio = models.DateTimeField()
    hora_fin = models.DateTimeField()

    def __str__(self):
        return f"{self.get_dia_semana_display()}: {self.hora_inicio} - {self.hora_fin}"

    
#Sesion Terapeutica
class SesionTerapeutica(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateField(default=timezone.now)
    actividades = models.TextField()
    tareas = models.TextField()
    fonoaudiologo = models.ForeignKey(Fonoaudiologo, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.fonoaudiologo} - {self.paciente} - {self.fecha} - {self.hora}'
    
    
#Formulario
class Formulario(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    numero = models.IntegerField()
    
    def __str__(self):
        return self.nombre
    
#Pregunta
class PreguntaFormulario(models.Model):
    id = models.AutoField(primary_key=True)
    textoPregunta = models.TextField()
    formulario = models.ForeignKey(Formulario, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.textoPregunta
    
#Respuesta
class RespuestaFormulario(models.Model):
    id = models.AutoField(primary_key=True)
    respuesta = models.TextField()
    pregunta = models.ForeignKey(PreguntaFormulario, on_delete=models.CASCADE)
    fechaRespuesta = models.DateField(default=timezone.now)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.respuesta
    
#OIRS
class OIRS(models.Model):
    TIPO_MENSAJE_CHOICES = [
        ('informacion', 'Información'),
        ('reclamo', 'Reclamo'),
        ('sugerencia', 'Sugerencia'),
    ]

    id = models.AutoField(primary_key=True)
    tipo_mensaje = models.CharField(max_length=20, choices=TIPO_MENSAJE_CHOICES)
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=9, blank=True)
    mensaje = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=10, default='Pendiente')
    respuesta = models.TextField(blank=True)
    fecha_respuesta = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.get_tipo_mensaje_display()} - {self.nombre}'