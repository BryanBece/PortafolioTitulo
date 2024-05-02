from django.shortcuts import render
from django.contrib import auth, messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from user.models import *
from .forms import *
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.http import JsonResponse
from datetime import datetime, timedelta, time


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
            messages.success(request, "Bienvenido " + user.nombre + " " + user.apellido)
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

# ------------------- Reserva de horas -------------------

#Calendario
def calendario(request):
    context = {
        'doctores': Fonoaudiologo.objects.all(),
    }
    return render(request, 'reservaHoras/calendario.html', context)

#Horas Disponibles
def ver_horas_disponibles(request):
    fecha_reserva_str = request.GET.get('fecha_reserva')
    doctor_id = request.GET.get('doctor_id')

    if fecha_reserva_str and doctor_id:
        # Convertir fecha_reserva de str a datetime
        fecha_reserva = datetime.strptime(fecha_reserva_str, '%d-%m-%Y')
        fecha_reserva_str_dd_mm_yyyy = fecha_reserva.strftime('%d/%m/%Y')
        

        # Obtener el doctor y las horas disponibles para esa fecha
        doctor = Fonoaudiologo.objects.get(pk=doctor_id)
        horas_disponibles = obtener_horas_disponibles_para_doctor(doctor, fecha_reserva)
        context = {
            'fecha_reserva': fecha_reserva_str,
            'fecha_reserva_dt': fecha_reserva_str_dd_mm_yyyy,
            'doctor': doctor,
            'horas_disponibles': horas_disponibles
        }
        return render(request, 'reservaHoras/horasDisponibles.html', context)
    else:
        # Si no se proporcionaron la fecha de reserva o el ID del doctor, redirigir a una página de error
        return render(request, 'reservaHoras/calendario.html')

def obtener_horas_disponibles_para_doctor(doctor, fecha_reserva):
    # Obtener las horas de trabajo del doctor para el día de la reserva
    dia_semana = fecha_reserva.weekday()
    horas_trabajo = HorasTrabajo.objects.filter(doctor=doctor, dia_semana=dia_semana)

    if horas_trabajo.exists():
        hora_inicio = horas_trabajo.first().hora_inicio
        hora_fin = horas_trabajo.first().hora_fin
    else:
        # Si el doctor no tiene horas de trabajo para el día de la reserva, retornar una lista vacía
        return []

    # Convertir hora_inicio y hora_fin a objetos datetime con la misma fecha que fecha_reserva
    fecha_inicio = datetime.combine(fecha_reserva, time())
    hora_inicio_dt = fecha_inicio.replace(hour=hora_inicio.hour, minute=hora_inicio.minute)
    hora_fin_dt = fecha_inicio.replace(hour=hora_fin.hour, minute=hora_fin.minute)

    # Crear una lista de todas las horas entre la hora de inicio y la hora de fin
    todas_las_horas = []
    hora_actual = hora_inicio_dt
    while hora_actual < hora_fin_dt:
        todas_las_horas.append(hora_actual)
        hora_actual += timedelta(hours=1)

    # Filtrar las horas disponibles eliminando las horas en las que ya hay citas reservadas para esa fecha
    citas = ReservaHora.objects.filter(fonoaudiologo=doctor, fecha=fecha_reserva)
    horas_reservadas = [cita.hora for cita in citas]
    horas_disponibles = [hora.strftime('%H:%M') for hora in todas_las_horas if hora not in horas_reservadas]

    return horas_disponibles

#Formulario de Reserva
def reservaHora(request):
    fecha_reserva = request.GET.get('fecha_reserva')
    print("Fecha" + str(fecha_reserva))
    doctor_id = request.GET.get('doctor_id')
    print(doctor_id)
    hora = request.GET.get('hora')
    print(hora)
    doctor = Fonoaudiologo.objects.get(pk=doctor_id)
    data = {
        'form': ReservaHoraForm(),
        'fecha_reserva': fecha_reserva,
        'hora': hora,
        'doctor': doctor
    }
    
    if request.method == 'POST':
        formulario = ReservaHoraForm(request.POST)
        if formulario.is_valid():
            nombre = formulario.cleaned_data.get('nombrePaciente')
            apellido = formulario.cleaned_data.get('apellidoPaciente')
            rut = formulario.cleaned_data.get('rutPaciente')
            telefono = formulario.cleaned_data.get('telefonoPaciente')
            email = formulario.cleaned_data.get('emailPaciente')
            
            res = ReservaHora()
            res.fecha = datetime.strptime(fecha_reserva, '%d-%m-%Y')
            res.hora = hora
            res.fonoaudiologo = doctor
            res.nombrePaciente = nombre
            res.apellidoPaciente = apellido
            res.rutPaciente = rut
            res.telefonoPaciente = telefono
            res.emailPaciente = email
            res.save()

            messages.success(request, 'Reserva realizada con éxito')
            return redirect('home')
        else:
            messages.error(request, 'Error al realizar la reserva')
            data["form"] = formulario
    
    return render(request, 'reservaHoras/reservaHora.html', data)


# ------------------- Reserva de horas -------------------

#Restablecer Contrseña
def restablecerContrasena(request, id, token):
    if request.method == 'POST':
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
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
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            try:
                token = default_token_generator.make_token(user)
                reset_url = reverse('restablecerContrasena', args=[user.id, token])
                subject = 'Restablecer Contraseña - COFAM'
                link = request.build_absolute_uri(reset_url)
                html_message = render_to_string('registration/reset_password_email.html', {'reset_url': link})

                send_mail(subject, None, settings.EMAIL_HOST_USER, [email], html_message=html_message)
                
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


#Comunas
def obtener_comunas(request):
    region_id = request.GET.get('region_id')
    comunas = Comuna.objects.filter(region_id=region_id).values('id', 'comuna')
    return JsonResponse(list(comunas), safe=False)

#Registro Paciente-Tutor
@login_required
def registroPacienteTutor(request):
    data ={
        "regiones" : Region.objects.all(),
        'formPac': RegistroPacienteForm(),
        'formTut': RegistroTutorForm()
    }
    
    if request.method == 'POST':
        formularioPaciente = RegistroPacienteForm(request.POST)
        formularioTutor = RegistroTutorForm(request.POST)
        if formularioPaciente.is_valid() and formularioTutor.is_valid():
            nombreTutor = formularioTutor.cleaned_data.get('nombre')
            apellidoTutor = formularioTutor.cleaned_data.get('apellido')
            correoTutor = formularioTutor.cleaned_data.get('email')
            
            if User.objects.filter(email=correoTutor).exists():
                messages.error(request, "El correo del tutor ya está registrado.")
            else:
                #Crear Tutor
                formularioTutor.save()
                
                tut = Tutor.objects.get(email=correoTutor)
                pac = Paciente()
                pac.nombre = formularioPaciente.cleaned_data.get('nombre')
                pac.apellido = formularioPaciente.cleaned_data.get('apellido')
                pac.rut = formularioPaciente.cleaned_data.get('rut')
                pac.fechaNacimiento = formularioPaciente.cleaned_data.get('fechaNacimiento')
                pac.genero = formularioPaciente.cleaned_data.get('genero')
                pac.telefono = formularioPaciente.cleaned_data.get('telefono')
                pac.direccion = formularioPaciente.cleaned_data.get('direccion')
                pac.comuna = formularioPaciente.cleaned_data.get('comuna')
                pac.tutor = tut
                pac.save()
                
                # Crear un nuevo usuario
                usuTut = User()
                usuTut.username = correoTutor
                usuTut.email = correoTutor
                usuTut.nombre = nombreTutor
                usuTut.apellido = apellidoTutor
                tipo_usuario_tutor = tipo_usuario.objects.get(nombre_tipo_usuario='Tutor')
                usuTut.tipoUsuario = tipo_usuario_tutor
                usuTut.save()
                
                messages.success(request, f'Paciente {pac.nombre} y Tutor {nombreTutor} creados')
                return redirect('perfil')
            
        else:
            data["formPac"] = formularioPaciente
            data["formTut"] = formularioTutor
    return render(request, 'registration/registroPacienteTutor.html', data)

