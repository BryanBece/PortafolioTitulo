from django import forms
from .models import *
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField


#Formulario de Registro Fonoaudiologo
class RegistroFonoForm(forms.ModelForm):
    class Meta:
        model = Fonoaudiologo
        fields = '__all__'
        exclude = ['id']
        labels = {
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'genero': 'Genero',
            'telefono': 'Telefono',
            'email': 'Email',
            'clinica': 'Clinica',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'clinica': forms.Select(attrs={'class': 'form-control'}),
        }
        
#Formulario de Registro Paciente
class RegistroPacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = '__all__'
        exclude = ['id', 'fonoaudiologo', 'tutor']
        labels = {
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'rut': 'Rut',
            'genero': 'Género',
            'telefono': 'Teléfono',
            'fechaNacimiento': 'Fecha de Nacimiento',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'fechaNacimiento': forms.DateInput(attrs={'class': 'form-control datepicker'}),
        }
        
#Formulario de Registro Tutor
class RegistroTutorForm(forms.ModelForm):
    class Meta:
        model = Tutor
        fields = '__all__'
        exclude = ['id']
        labels = {
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'rut': 'Rut',
            'genero': 'Genero',
            'telefono': 'Telefono',
            'email': 'Email',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        
#Formulario de Registro de Reserva
class ReservaHoraForm(forms.ModelForm):
    class Meta:
        model = ReservaHora
        fields = '__all__'
        exclude = ['id', 'fecha', 'hora', 'fonoaudiologo', 'estado']
        labels = {
            'nombrePaciente': 'Nombre Paciente',
            'apellidoPaciente': 'Apellido Paciente',
            'rutPaciente': 'Rut',
            'telefonoPaciente': 'Teléfono',
            'emailPaciente': 'Email',
        }

    def __init__(self, *args, **kwargs):
        horarios_disponibles = kwargs.pop('horarios_disponibles', None)
        super(ReservaHoraForm, self).__init__(*args, **kwargs)
        if horarios_disponibles:
            self.fields['hora'].choices = [(horario.id, horario.hora.strftime('%H:%M')) for horario in horarios_disponibles]

class PreguntasForm(forms.ModelForm):
    class Meta:
        model = PreguntaFormulario
        fields = '__all__'
        exclude = ['id']
        
        
class SesionForm(forms.ModelForm):
    class Meta:
        model = SesionTerapeutica
        fields = '__all__'
        exclude = ['id', 'fecha', 'fonoaudiologo', 'paciente', 'tutor']
        labels = {
            'tareas': 'Tareas asignadas para el domicilio',
            'actividades': 'Actividades realizadas en la sesión',
        }
