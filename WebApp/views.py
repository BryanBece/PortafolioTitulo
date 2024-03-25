from django.shortcuts import render

# Create your views here.


#Vista home
def home(request):
    return render(request, 'home.html')