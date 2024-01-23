from django.shortcuts import render
from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import *
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
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

def alumno_pest(request):
    query = request.GET.get('q')
    if query:
        # Realiza la búsqueda utilizando el campo 'nombre' o 'apellido' o clave o grupo
        alumnos = alumno.objects.filter(Q(nombre__icontains=query) | Q(apellido__icontains=query)|Q(clave__icontains=query) |Q(grupo__icontains=query) )
    else:
        # Si no hay búsqueda, muestra todos los alumnos
        alumnos = alumno.objects.all()

    return render(request, "alumnos.html", {"current_tab": "alumno", "alumnos": alumnos})


def agregar_alum(request):
    alumno_item= alumno(clave=request.POST['clave'],
                        nombre=request.POST['nombre'],
                        apellido=request.POST['apellido'],
                        grupo=request.POST['grupo'],)
    alumno_item.save()
    return redirect('/alumno')

def alumno_detalle(request, pk):
    # Usamos get_object_or_404 para obtener el objeto alumno o retornar un error 404 si no se encuentra
    alumno_obj = get_object_or_404(alumno, pk=pk)
    
    return render(request, 'alumno_detalle.html', {'alumno': alumno_obj})

from django.shortcuts import render, get_object_or_404, redirect

# ... tus funciones existentes ...

def editar_alumno(request, pk):
    # Usamos get_object_or_404 para obtener el objeto alumno o retornar un error 404 si no se encuentra
    alumno_obj = get_object_or_404(alumno, pk=pk)

    if request.method == 'POST':
        # Procesa el formulario de edición aquí
        alumno_obj.nombre = request.POST['nombre']
        alumno_obj.apellido = request.POST['apellido']
        alumno_obj.clave = request.POST['clave']
        alumno_obj.grupo = request.POST['grupo']
        alumno_obj.save()

        # Después de guardar los cambios, redirige a la página de alumnos
        return redirect('/alumno')

    return render(request, 'editar_alumno.html', {'alumno': alumno_obj})

def eliminar_alumno(request, pk):
    alumno_obj = get_object_or_404(alumno, pk=pk)

    if request.method == 'POST':
        # Utiliza el método delete() en el queryset, no en la instancia del modelo
        alumno.objects.filter(pk=pk).delete()

        # Después de eliminar, redirige a la página de alumnos
        return redirect('/alumno')

    return render(request, 'eliminar_alumno.html', {'alumno': alumno_obj})