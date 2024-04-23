from django.shortcuts import render
from django.contrib import auth, messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from user.models import *
from .forms import *
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect

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

#Restablecer Contrseña
def restablecerContrasena(request, id, token):
    if request.method == 'POST':
        password = request.POST.get('contrasena')
        password2 = request.POST.get('confirmar_contrasena')
        
        if password == password2:
            user = User.objects.get(id=id)
            if default_token_generator.check_token(user, token):
                user.set_password(password)
                user.save()
                messages.success(request, 'Contraseña restablecida con éxito')
                return redirect('login')
            else:
                messages.error(request, 'Token inválido')
        else:
            messages.error(request, 'Las contraseñas no coinciden')
    
    return render(request, 'registration/restablecerContrasena.html')

#Reset Contraseña Home
def resetearContrasena(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print(email)
        if User.objects.filter(email=email).exists():
            #Obtener ID del usuario
            user = User.objects.get(email=email)
            print("User: ", user)
            try:
                token = default_token_generator.make_token(user)
                print("Token: ", token)
                reset_url = reverse('restablecerContrasena', args=[user.id, token])
                print("Reset URL: ", reset_url)
                
                subject = 'Restablecer contraseña'
                message = f'Para restablecer tu contraseña, haz clic en el siguiente enlace: {request.build_absolute_uri(reset_url)}'
                print("Message: ", message)
                from_email = settings.EMAIL_HOST_USER
                print("From Email: ", from_email)
                recipient_list = [email]
                print("Recipient List: ", recipient_list)
                
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                             
                messages.success(request, 'Correo enviado con éxito.')
            
            except Exception as e:
                messages.error(request, 'Error al enviar el correo')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, 'El correo no está registrado')
    
    return render(request, 'registration/resetearContrasena.html')
   


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