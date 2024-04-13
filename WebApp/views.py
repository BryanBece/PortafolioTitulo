from django.shortcuts import render
from django.contrib import auth, messages
from django.shortcuts import render, redirect

# Create your views here.

#NOMENCLATURA CAMELCASE ejemplo: estoEsUnEjemplo

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
            print("Usuario autenticado")
            messages.success(request, "Bienvenido")
            return redirect("perfil") 
        else:
            print("Credenciales incorrectas")
            messages.error(request, "Credenciales incorrectas")

    return render(request, 'registration/login.html')

#Logout
def logout(request):
    auth.logout(request)
    return redirect("home")

#Vista Perfil
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