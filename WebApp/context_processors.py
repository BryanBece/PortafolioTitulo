from .models import Mensaje

def mensajesNoLeidos(request):
    if request.user.is_authenticated:
        fonoaudiologo = getattr(request.user, 'fonoaudiologo', None)
        if fonoaudiologo:
            mensajesNoLeidos = Mensaje.objects.filter(fonoaudiologo=fonoaudiologo, leido=False).count()
            return {'mensajesNoLeidos': mensajesNoLeidos}
    return {}
