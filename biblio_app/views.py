from django.shortcuts import render
from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import *
from django.db.models import Q
import pandas as pd
from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime
from django.core.exceptions import ValidationError

#register your models here

# Create your views here.
def inicio(request):
    return render(request,"inicio.html",context={"current_tab": "inicio"})
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

def cargar_desde_excel(request):
    if request.method == 'POST':
        if 'excel_file' in request.FILES:
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file)

            # Verificar si todas las columnas necesarias están presentes en el DataFrame
            required_columns = ['clave', 'nombre', 'apellido', 'grupo']
            missing_columns = [col for col in required_columns if col not in df.columns]

            if missing_columns:
                missing_columns_str = ', '.join(missing_columns)
                return HttpResponse(f"El archivo Excel no tiene las columnas necesarias: {missing_columns_str}.")

            for index, row in df.iterrows():
                alumno_item = alumno(
                    clave=row['clave'],
                    nombre=row['nombre'],
                    apellido=row['apellido'],
                    grupo=row['grupo'],
                )
                alumno_item.save()

            return redirect('/alumno')

    return render(request, 'tu_template_excel.html')

def borrar_todos_los_alumnos(request):
    if request.method == 'GET':
        # Realiza la lógica para borrar todos los registros de la tabla de alumnos
        alumno.objects.all().delete()

        # Redirige de vuelta a la página de alumnos
        return redirect('/alumno')

    return HttpResponse("Solicitud no válida.")

def libros_pest(request):
    query = request.GET.get('q')
    if query:
        # Realiza la búsqueda utilizando el campo 'nombre' o 'apellido' o clave o grupo
        libros = libro.objects.filter(Q(codigolibro__icontains=query) | Q(titulo__icontains=query)|Q(autor__icontains=query) |Q(editorial__icontains=query) )
    else:
        # Si no hay búsqueda, muestra todos los alumnos
        libros = libro.objects.all()

    return render(request,"libros.html",context={"current_tab": "libro", "libros": libros})

def agregar_libros(request):
    fechapubl_str = request.POST.get('fechapubl', '')
    if fechapubl_str:
        try:
            fechapubl = datetime.strptime(fechapubl_str, '%Y-%m-%d').date()
        except ValueError:
            # Handle invalid date format
            raise ValidationError('Invalid date format. Please use YYYY-MM-DD.')
    else:
        # Handle case where date is empty
        fechapubl = None
    libro_item= libro(codigolibro=request.POST['clave'],
                        titulo=request.POST['titulo'],
                        autor=request.POST['autor'],
                        ilustrador=request.POST['ilustrador'],
                        editorial=request.POST['editorial'],
                        numerotomo=request.POST['numtomo'],
                        ubicacionbiblio=request.POST['ubicacion'],
                        publicodirigido=request.POST['publico'],
                        fechapublicacion=fechapubl,
                        caracteristicasespeciales=request.POST['caracteristicas'],
                        disponible=True)
    libro_item.save()
    return redirect('/libro')

def libro_detalle(request, codigolibro):
    # Usamos get_object_or_404 para obtener el objeto alumno o retornar un error 404 si no se encuentra
    libro_obj = get_object_or_404(libro, codigolibro=codigolibro)
    
    return render(request, 'libros_detalle.html', {'libro': libro_obj})



def editar_libro(request, codigolibro):
    # Usamos get_object_or_404 para obtener el objeto libro o retornar un error 404 si no se encuentra
    libro_obj = get_object_or_404(libro, codigolibro=codigolibro)

    if request.method == 'POST':
        # Procesa el formulario de edición aquí
        libro_obj.titulo = request.POST['titulo']
        libro_obj.autor = request.POST['autor']
        libro_obj.ilustrador = request.POST['ilustrador']

        # Convertir la fecha al formato esperado
        try:
            fechapublicacion = datetime.strptime(request.POST['fechapublicacion'], '%b. %d, %Y').strftime('%Y-%m-%d')
            libro_obj.fechapublicacion = fechapublicacion
        except ValueError:
            return HttpResponse("Invalid date format. Please enter the date in the format 'Mon. Day, Year'.")

        libro_obj.editorial = request.POST['editorial']
        libro_obj.numerotomo = request.POST['numerotomo']
        libro_obj.caracteristicasespeciales = request.POST['caracteristicasespeciales']

        # Convertir 'on' to True, otherwise set to False
        libro_obj.disponible = request.POST.get('disponible') == 'on'

        libro_obj.ubicacionbiblio = request.POST['ubicacionbiblio']
        libro_obj.publicodirigido = request.POST['publicodirigido']
        libro_obj.save()

        # Después de guardar los cambios, redirige a la página de libros
        return redirect('/libro')

    return render(request, 'editar_libro.html', {'libro': libro_obj})


def eliminar_libro(request, codigolibro):
    libro_obj = get_object_or_404(libro, codigolibro=codigolibro)

    if request.method == 'POST':
        # Utiliza el método delete() en el queryset, no en la instancia del modelo
        libro.objects.filter(codigolibro=codigolibro).delete()

        # Después de eliminar, redirige a la página de libros
        return redirect('/libro')

    return render(request, 'eliminar_libro.html', {'libro': libro_obj})

def cargar_desde_excel_libro(request):
    if request.method == 'POST':
        if 'excel_file' in request.FILES:
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file)

            # Verificar si todas las columnas obligatorias están presentes en el DataFrame
            required_columns = ['codigolibro', 'titulo', 'autor', 'editorial']
            missing_columns = [col for col in required_columns if col not in df.columns]

            if missing_columns:
                missing_columns_str = ', '.join(missing_columns)
                return HttpResponse(f"El archivo Excel no tiene las columnas obligatorias: {missing_columns_str}.")

            for index, row in df.iterrows():
                # Verificar campos obligatorios
                if any(pd.isna(row[col]) for col in required_columns):
                    return HttpResponse("Los campos obligatorios no pueden estar vacíos.")

                # Establecer valor por defecto para fechapublicacion si está ausente
                fechapublicacion = row.get('fechapublicacion', datetime.now().date())

                libro_item = libro(
                    codigolibro=row['codigolibro'],
                    titulo=row['titulo'],
                    autor=row['autor'],
                    editorial=row['editorial'],
                    ilustrador=row.get('ilustrador', ''),
                    fechapublicacion=fechapublicacion,
                    numerotomo=row.get('tomo', ''),
                    caracteristicasespeciales=row.get('caracteristicas', ''),
                    disponible=True,
                    ubicacionbiblio=row.get('ubicacionbiblio', ''),
                    publicodirigido=row.get('publico', ''),
                    # Agrega otros campos según sea necesario
                )
                libro_item.save()

            return redirect('/libro')

    return render(request, 'tu_template_excel.html')


def borrar_todos_los_libros(request):
    if request.method == 'GET':
        # Realiza la lógica para borrar todos los registros de la tabla de alumnos
        libro.objects.all().delete()

        # Redirige de vuelta a la página de alumnos
        return redirect('/libro')

    return HttpResponse("Solicitud no válida.")
def eliminar_libros_por_titulo(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo', None)

        if titulo:
            # Utiliza el método delete() en el queryset para eliminar todos los libros con el mismo título
            libro.objects.filter(titulo=titulo).delete()

    return redirect('/libro')