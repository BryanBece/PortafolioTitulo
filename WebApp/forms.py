from django import forms
from .models import *


#Formulario de Registro Fonoaudiologo
class RegistroFonoForm(forms.ModelForm):
    class Meta:
        model = Fonoaudiologo
        fields = '__all__'
        exclude = ['id']
        labels = {
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'rut': 'Rut',
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