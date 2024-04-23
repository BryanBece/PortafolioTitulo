from django.shortcuts import render
from django.contrib import auth, messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from user.models import *
from .forms import *

# Create your views here.

#NOMENCLATURA CAMELCASE ejemplo: estoEsUnEjemplo
#Prueba

#Vista home
def home(request):
    return render(request, 'home.html')

# Vista Login
def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        print(email, password)

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "Bienvenido")
            return redirect("perfil") 
        else:
            messages.error(request, "Credenciales incorrectas")

    return render(request, 'registration/login.html')

#Logout
@login_required
def logout(request):
    auth.logout(request)
    return redirect("home")

#Vista Perfil
@login_required
def perfil(request):
    return render(request, 'perfil.html')

#Vista Equipo
def equipo(request):
    return render(request, 'equipo.html')

#Vista Nosotros
def nosotros(request):
    return render(request, 'nosotros.html')

#Vista OIRS
def oirs(request):
    return render(request, 'oirs.html')

#Vista Reserva
def reserva(request):
    return render(request, 'reserva.html')


#Registro Fonoaudiologos
def registroFono(request):
    data = {
        'form': RegistroFonoForm()
    }
    
    if request.method == 'POST':
        formulario = RegistroFonoForm(request.POST)
        if formulario.is_valid():
            nombre = formulario.cleaned_data.get('nombre')
            apellido = formulario.cleaned_data.get('apellido')
            correo = formulario.cleaned_data.get('email')
            rut = formulario.cleaned_data.get('rut')
            genero = formulario.cleaned_data.get('genero')
            telefono = formulario.cleaned_data.get('telefono')
            clinica = formulario.cleaned_data.get('clinica')
            
            if User.objects.filter(email=correo).exists():
                messages.error(request, "El correo ya está registrado.")
            else:
                #Crear Fono
                formulario.save()
    
                # Crear un nuevo usuario
                usu = User()
                usu.username = correo
                usu.email = correo
                usu.nombre = nombre
                usu.apellido = apellido
                tipo_usuario_fonoaudiologo = tipo_usuario.objects.get(nombre_tipo_usuario='Fonoaudiologo')
                usu.tipoUsuario = tipo_usuario_fonoaudiologo
                usu.save() 
                messages.success(request, f'Fonoaudiologo {nombre} creado')
                return redirect('perfil')
            
        else:
            data["form"] = formulario
    
    return render(request, 'registration/registroFono.html', data)