from .models import Mensaje, OIRS

def mensajesNoLeidos(request):
    if request.user.is_authenticated:
        receptor = f"{request.user.nombre} {request.user.apellido}"
        mensajesNoLeidos = Mensaje.objects.filter(receptor=receptor, leidoUno=False).count() + \
                           Mensaje.objects.filter(receptor=receptor, leidoDos=False).count()
        return {'mensajesNoLeidos': mensajesNoLeidos}
    return {}

def oirsPendientes(request):
    if request.user.is_authenticated:
        oirsPendientes = OIRS.objects.filter(estado='Pendiente').count()
        return {'oirsPendientes': oirsPendientes}
    return {}