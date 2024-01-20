from django.shortcuts import render
from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

#register your models here

# Create your views here.
def inicio(request):
    return render(request,"inicio.html",context={"current_tab": "inicio"})
def alumno(request):
    return render(request,"alumnos.html",context={"current_tab": "alumno"})
def libro(request):
    return render(request,"libros.html",context={"current_tab": "libro"})
def busqueda(request):
    return render(request,"busqueda.html",context={"current_tab": "busqueda"})
def prestamo(request):
    return render(request,"prestamo.html",context={"current_tab": "prestamo"})
def retorno(request):
    return render(request,"retorno.html",context={"current_tab": "retorno"})
def multa(request):
    return render(request,"multas.html",context={"current_tab": "multa"})
def etiqueta(request):
    return render(request,"etiqueta.html",context={"current_tab": "etiqueta"})

def iniciar_sesion(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        contrasena = request.POST.get('contrasena')

        user = authenticate(request, username=usuario, password=contrasena)

        if user is not None:
            login(request, user)
            print(f'Inicio de sesión exitoso: {user.username}')
            return redirect('inicio')
        else:
            print(f'Credenciales incorrectas: {usuario} {contrasena}')
            messages.error(request, 'Credenciales incorrectas. Intenta de nuevo.')

    return render(request, 'inicio.html', context={"current_tab": "inicio"})

def cerrar_sesion(request):
    logout(request)
    return redirect('inicio')
