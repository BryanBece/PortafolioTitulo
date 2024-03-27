from django.shortcuts import render

# Create your views here.

#NOMENCLATURA CAMELCASE ejemplo: monicaNovoa

#Vista home
def home(request):
    return render(request, 'home.html')