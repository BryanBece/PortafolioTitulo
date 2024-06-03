from django import forms
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit



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
            'antecedentesMedicos': 'Antecedentes Médicos',
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


class OIRSMensajeForm(forms.ModelForm):
    class Meta:
        model = OIRS
        fields = ['tipo_mensaje', 'nombre', 'email', 'telefono', 'mensaje']
        widgets = {
            'tipo_mensaje': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Tipo de Mensaje'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su nombre'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su email'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su número de celular'}),
            'mensaje': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingrese su mensaje'}),
            
        }

    def __init__(self, *args, **kwargs):
        super(OIRSMensajeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Enviar'))
        
#Formulario de Respuesta OIRS
class OIRSRespuestaForm(forms.ModelForm):
    class Meta:
        model = OIRS
        fields = ['respuesta']
        
#Notas Paciente
class NotasPacienteForm(forms.ModelForm):
    class Meta:
        model = NotaPaciente
        fields = '__all__'
        exclude = ['id', 'paciente', 'fecha']
        labels = {
            'nota': 'Nota',
        }
        widgets = {
            'nota': forms.Textarea(attrs={'class': 'form-control'}),
        }