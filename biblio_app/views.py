from django.shortcuts import render
from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import *
#register your models here

# Create your views here.
def inicio(request):
    return render(request,"inicio.html",context={"current_tab": "inicio"})
def alumnos(request):
    return render(request,"alumnos.html",context={"current_tab": "alumno"})
def libros(request):
    return render(request,"libros.html",context={"current_tab": "libro"})
def busquedas(request):
    return render(request,"busqueda.html",context={"current_tab": "busqueda"})
def prestamos(request):
    return render(request,"prestamo.html",context={"current_tab": "prestamo"})
def retornos(request):
    return render(request,"retorno.html",context={"current_tab": "retorno"})
def multas(request):
    return render(request,"multas.html",context={"current_tab": "multa"})
def etiquetas(request):
    return render(request,"etiqueta.html",context={"current_tab": "etiqueta"})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('')  # Redirige a la URL deseada después del inicio de sesión
        else:
            # Lógica para manejar credenciales incorrectas
            messages.error(request, 'Credenciales incorrectas. Por favor, inténtalo de nuevo.')
            pass

    return render(request, 'login.html')

def alumo_pest(request):
    alumnos = alumno.objects.all()
    return render(request,request,"alumnos.html",context={"current_tab": "alumno","alumnos":alumnos})