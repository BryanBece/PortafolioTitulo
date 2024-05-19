from django.shortcuts import render
from django.contrib import auth, messages
from django.shortcuts import render, redirect, get_object_or_404
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
from datetime import datetime, timedelta, time, date



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
    if request.user.tipoUsuario.nombre_tipo_usuario in ["Fonoaudiologo", "Gerencia", "Tutor"]:
        tomorrow = date.today() + timedelta(days=1)
        reservas_futuras = ReservaHora.objects.filter(fecha__gte=tomorrow).filter(estado='Reservada').order_by('-id')
        
        data = {
            'reservas_hoy': ReservaHora.objects.filter(fecha__gte=date.today()).filter(estado='Reservada').order_by('-id'),
            'reservas_total': ReservaHora.objects.exclude(estado='Reservada').order_by('-id'),
            'reservas_futuras': reservas_futuras,
        }
        return render(request, 'perfil.html', data)
    else:
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
        fecha_reserva = datetime.strptime(fecha_reserva_str, '%d-%m-%Y')
        fecha_reserva_str_dd_mm_yyyy = fecha_reserva.strftime('%d/%m/%Y')
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
        messages.error(request, 'Debe seleccionar una fecha y un doctor para ver las horas disponibles')
        return redirect('calendario')

def obtener_horas_disponibles_para_doctor(doctor, fecha_reserva):
    dia_semana = fecha_reserva.weekday()
    horas_trabajo = HorasTrabajo.objects.filter(doctor=doctor, dia_semana=dia_semana)

    if horas_trabajo.exists():
        hora_inicio = horas_trabajo.first().hora_inicio
        hora_fin = horas_trabajo.first().hora_fin
    else:
        return []
    fecha_inicio = datetime.combine(fecha_reserva, time())
    hora_inicio_dt = fecha_inicio.replace(hour=hora_inicio.hour, minute=hora_inicio.minute)
    hora_fin_dt = fecha_inicio.replace(hour=hora_fin.hour, minute=hora_fin.minute)

    todas_las_horas = []
    hora_actual = hora_inicio_dt
    while hora_actual < hora_fin_dt:
        todas_las_horas.append(hora_actual.strftime('%H:%M'))
        hora_actual += timedelta(hours=1)

    citas = ReservaHora.objects.filter(fonoaudiologo=doctor, fecha=fecha_reserva)
    horas_reservadas = [cita.hora.strftime('%H:%M') for cita in citas]
    horas_disponibles = [hora for hora in todas_las_horas if hora not in horas_reservadas]

    return horas_disponibles


#Formulario de Reserva
def reservaHora(request):
    fecha_reserva = request.GET.get('fecha')
    doctor_id = request.GET.get('fonoaudiologo')
    hora = request.GET.get('hora')
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
            
            try:
                subject = 'Confirmación Reserva De Hora - COFAM'
                html_message = render_to_string('reservaHoras/confirmacionCorreo.html', {'fecha': fecha_reserva, 'hora': hora, 'fonoaudiologo': doctor, 'nombre': nombre, 'apellido': apellido, 'rut': rut})
                send_mail(subject, None, settings.EMAIL_HOST_USER, [email], html_message=html_message)
                
            except Exception as e:
                messages.error(request, 'Error al enviar el correo')

            messages.success(request, 'Reserva realizada con éxito')
            return redirect('home')
        else:
            messages.error(request, 'Error al realizar la reserva')
            data["form"] = formulario
    
    return render(request, 'reservaHoras/reservaHora.html', data)

#Cancelar Reserva
@login_required
def cancelarReserva(request, id):
    reserva = ReservaHora.objects.get(id=id)
    fecha_reserva = reserva.fecha.strftime('%d-%m-%Y')
    hora = reserva.hora
    doctor = reserva.fonoaudiologo
    nombre = reserva.nombrePaciente
    apellido = reserva.apellidoPaciente
    rut = reserva.rutPaciente
    email = reserva.emailPaciente
    
    try:
        subject = 'Cancelación Reserva De Hora - COFAM'
        html_message = render_to_string('reservaHoras/cancelarCorreo.html', {'fecha': fecha_reserva, 'hora': hora, 'fonoaudiologo': doctor, 'nombre': nombre, 'apellido': apellido, 'rut': rut})
        send_mail(subject, None, settings.EMAIL_HOST_USER, [email], html_message=html_message)
        reserva.delete()
    
        messages.success(request, 'Reserva cancelada con éxito')
                
    except Exception as e:
        messages.error(request, 'Error al cancelar la hora')
    
    return redirect('perfil')

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
@login_required
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
        'formTut': RegistroTutorForm(),
        'rut': request.GET.get('rut')
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
                return redirect('ficha_clinica', id=pac.id)
            
        else:
            data["formPac"] = formularioPaciente
            data["formTut"] = formularioTutor
    return render(request, 'registration/registroPacienteTutor.html', data)

# ------------------- Formularios Evaluación -------------------

#Vista Preguntas
@login_required
def preguntas(request):
    Preguntas = PreguntaFormulario.objects.all()
    data = {
        "preguntas": Preguntas,
    }
    return render(request, 'formularios/preguntas.html', data)

#Crear preguntas
@login_required
def crearPreguntas(request):
    data = {"form": PreguntasForm()}

    if request.method == "POST":
        formulario = PreguntasForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Pregunta Creada Correctamente")
            return redirect(to="preguntas")
        else:
            data["form"] = formulario
    return render(request, 'formularios/crearPreguntas.html', data)

#Modificar preguntas
login_required
def modificarPreguntas(request,id):
    Preguntas = PreguntaFormulario.objects.get(id=id)
    data = {"form": PreguntasForm(instance=Preguntas)}

    if request.method == "POST":
        formulario = PreguntasForm(
            data=request.POST, instance=Preguntas)
        
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado Correctamente")
            return redirect(to="preguntas")
        data["form"] = formulario
    return render(request, 'formularios/modificarPreguntas.html', data)

#Eliminar preguntas
@login_required
def eliminarPreguntas(request, id):
    Preguntas = PreguntaFormulario.objects.get(id=id)
    Preguntas.delete()
    messages.success(request, "Eliminado Correctamente")
    return redirect(to="preguntas")

# ------------------- Formularios Evaluación -------------------

#Sesion Asistida
@login_required
def sesionAsistida(request, id):
    reserva = ReservaHora.objects.get(id=id)
    reserva.estado = 'Asistida'
    reserva.save()
    messages.success(request, "Guardada Correctamente")
    return redirect(to="perfil")

#Sesión No Asistida
@login_required
def sesionNoAsistida(request, id):
    reserva = ReservaHora.objects.get(id=id)
    reserva.estado = 'No Asistid'
    reserva.save()
    messages.success(request, "Guardada Correctamente")
    return redirect(to="perfil")

#Ficha Clinica
@login_required
def fichaClinica(request, id):
    paciente = Paciente.objects.get(id=id)
    sesionFono = SesionTerapeutica.objects.filter(paciente=paciente).order_by('-id')
    data = {
        'paciente': paciente,
        'sesiones': sesionFono,
    }
    
    return render(request, 'atencion/fichaClinica.html', data)

#Buscar Paciente
@login_required
def busquedaPaciente(request):
    rut = request.GET.get('rut')
    return render(request, 'atencion/buscarPaciente.html', {'rut': rut})

def buscar_paciente(request):
    rut = request.GET.get('rut')
    
    if rut:
        try:
            paciente = Paciente.objects.get(rut=rut)
            messages.success(request, 'Paciente encontrado')
            url = reverse('fichaClinica', args=[paciente.id])
            return JsonResponse({'found': True, 'url': url})
        except Paciente.DoesNotExist:
            return JsonResponse({'found': False})
    
    return JsonResponse({'found': False})

#Sesión Fonoaudiologica
@login_required
def sesionFono(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    fono = Fonoaudiologo.objects.get(email=request.user.email)
    data = {
        'form': SesionForm(),
        'paciente': paciente
    }
    
    if request.method == 'POST':
        form = SesionForm(request.POST)
        if form.is_valid():
            sesion = form.save(commit=False)
            sesion.fonoaudiologo = fono
            sesion.paciente = paciente
            sesion.tutor = paciente.tutor
            sesion.fecha = timezone.now()
            sesion.save()
            
            try:
                subject = 'Detalle de Sesión Fonoaudiológica'
                html_message = render_to_string('atencion/detalleSesionEmail.html', {'sesion': sesion})
                send_mail(subject, None, settings.EMAIL_HOST_USER, [paciente.tutor.email], html_message=html_message)
    
                messages.success(request, 'Sesión guardada correctamente, el correo ha sido enviado al tutor')
                
            except Exception as e:
                messages.error(request, 'Error al guardar la sesión')
            
            return redirect('fichaClinica', id=paciente.id)  
    else:
        form = SesionForm(initial={'paciente': paciente, 'tutor': paciente.tutor})
        
    return render(request, 'atencion/sesion.html', data)

@login_required
def detalleSesion(request, id):
    sesion = get_object_or_404(SesionTerapeutica, id=id)
    return render(request, 'atencion/detalleSesion.html', {'sesion': sesion})
