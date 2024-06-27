from django import forms
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

# Formulario de Registro Fonoaudiologo
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
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'rut': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'genero': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': 'required'}),
            'clinica': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
        }

# Formulario de Registro Paciente
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
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'rut': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'genero': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': 'required'}),
            'fechaNacimiento': forms.DateInput(attrs={'class': 'form-control datepicker', 'required': 'required'}),
        }

# Formulario de Registro Tutor
class RegistroTutorForm(forms.ModelForm):
    class Meta:
        model = Tutor
        fields = '__all__'
        exclude = ['id']
        labels = {
            'nombreTutor': 'Nombre',
            'apellidoTutor': 'Apellido',
            'rutTutor': 'Rut',
            'generoTutor': 'Genero',
            'telefonoTutor': 'Telefono',
            'emailTutor': 'Email',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'rut': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'genero': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': 'required'}),
        }

# Formulario de Registro de Reserva
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
        widgets = {
            'nombrePaciente': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'apellidoPaciente': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'rutPaciente': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'telefonoPaciente': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'emailPaciente': forms.EmailInput(attrs={'class': 'form-control', 'required': 'required'}),
        }

    def __init__(self, *args, **kwargs):
        horarios_disponibles = kwargs.pop('horarios_disponibles', None)
        super(ReservaHoraForm, self).__init__(*args, **kwargs)
        if horarios_disponibles:
            self.fields['hora'].choices = [(horario.id, horario.hora.strftime('%H:%M')) for horario in horarios_disponibles]

# Formulario Preguntas
class PreguntasForm(forms.ModelForm):
    class Meta:
        model = PreguntaFormulario
        fields = '__all__'
        exclude = ['id']
        widgets = {
            field: forms.TextInput(attrs={'class': 'form-control', 'required': 'required'})
            for field in '__all__'
        }

# Formulario de Sesion 
class SesionForm(forms.ModelForm):
    class Meta:
        model = SesionTerapeutica
        fields = '__all__'
        exclude = ['id', 'fecha', 'fonoaudiologo', 'paciente', 'tutor']
        labels = {
            'tareas': 'Tareas asignadas para el domicilio',
            'actividades': 'Actividades realizadas en la sesión',
        }
        widgets = {
            'tareas': forms.Textarea(attrs={'class': 'form-control', 'required': 'required'}),
            'actividades': forms.Textarea(attrs={'class': 'form-control', 'required': 'required'}),
        }

# Formulario OIRS
class OIRSMensajeForm(forms.ModelForm):
    class Meta:
        model = OIRS
        fields = ['tipo_mensaje', 'nombre', 'email', 'telefono', 'mensaje']
        widgets = {
            'tipo_mensaje': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Tipo de Mensaje', 'required': 'required'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su nombre', 'required': 'required'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su email', 'required': 'required'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su número de celular', 'required': 'required'}),
            'mensaje': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingrese su mensaje', 'required': 'required'}),
        }

    def __init__(self, *args, **kwargs):
        super(OIRSMensajeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Enviar'))

# Formulario de Respuesta OIRS
class OIRSRespuestaForm(forms.ModelForm):
    class Meta:
        model = OIRS
        fields = ['respuesta']
        widgets = {
            'respuesta': forms.Textarea(attrs={'class': 'form-control', 'required': 'required'})
        }

# Notas Paciente
class NotasPacienteForm(forms.ModelForm):
    class Meta:
        model = NotaPaciente
        fields = '__all__'
        exclude = ['id', 'paciente', 'fecha']
        labels = {
            'nota': 'Nota',
        }
        widgets = {
            'nota': forms.Textarea(attrs={'class': 'form-control', 'required': 'required'}),
        }

# Formulario Mensaje
class MensajeForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = ['texto']
        labels = {
            'texto': 'Mensaje',
        }
        widgets = {
            'texto': forms.Textarea(attrs={'class': 'form-control', 'required': 'required'})
        }
