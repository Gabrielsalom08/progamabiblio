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
from django.http import JsonResponse

#register your models here

# Create your views here.
def inicio(request):
    return render(request,"inicio.html",context={"current_tab": "inicio"})
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
        # Realiza la búsqueda utilizando el campo 'nombre', 'apellido', 'clave' o 'grupo'
        alumnos = Alumno.objects.filter(
            Q(nombre__icontains=query) |
            Q(apellido__icontains=query) |
            Q(nombre__icontains=query.split()[0]) &  # Busca el primer nombre
            Q(apellido__icontains=query.split()[-1]) |# Busca el último nombre
            Q(clave__icontains=query) |
            Q(grupo__icontains=query)
        ).distinct()
    else:
        # Si no hay búsqueda, muestra todos los alumnos
        alumnos = Alumno.objects.all()

    return render(request, "alumnos.html", {"current_tab": "alumno", "alumnos": alumnos})


def agregar_alum(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        grupo = request.POST.get('grupo')

        # Verificar si los campos obligatorios no están vacíos
        if not nombre or not apellido or not grupo:
            return render(request, 'error.html', {'mensaje': 'Por favor, completa todos los campos obligatorios.'})

        try:
            # Intentar crear una instancia de Alumno con los datos proporcionados
            alumno_item = Alumno(nombre=nombre, apellido=apellido, grupo=grupo)
            alumno_item.full_clean()  # Validar los datos del modelo
            alumno_item.save()  # Guardar el objeto en la base de datos
            return redirect('/alumno')
        except ValidationError as e:
            # Si se produce una excepción de validación, mostrar un mensaje de error
            return render(request, 'error.html', {'mensaje': '; '.join(e.messages)})

    return render(request, 'formulario_alumno.html')

def alumno_detalle(request, pk):
    alumno_obj = get_object_or_404(Alumno, clave=pk)
    return render(request, 'alumno_detalle.html', {'alumno': alumno_obj})

def editar_alumno(request, pk):
    alumno_obj = get_object_or_404(Alumno, clave=pk)

    if request.method == 'POST':
        alumno_obj.nombre = request.POST['nombre']
        alumno_obj.apellido = request.POST['apellido']
        alumno_obj.grupo = request.POST['grupo']
        alumno_obj.save()
        return redirect('/alumno')

    return render(request, 'editar_alumno.html', {'alumno': alumno_obj})

def eliminar_alumno(request, pk):
    alumno_obj = get_object_or_404(Alumno, clave=pk)
    print(alumno_obj)

    if request.method == 'POST':
        alumno_obj.delete()
        return redirect('/alumno')

    return render(request, 'borrar_alumno.html', {'alumno': alumno_obj})

def cargar_desde_excel(request):
    if request.method == 'POST' and 'excel_file' in request.FILES:
        excel_file = request.FILES['excel_file']
        df = pd.read_excel(excel_file)

        required_columns = ['nombre', 'apellido', 'grupo']
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            missing_columns_str = ', '.join(missing_columns)
            return HttpResponse(f"El archivo Excel no tiene las columnas necesarias: {missing_columns_str}.")

        for index, row in df.iterrows():
            alumno_item = Alumno(
                nombre=row['nombre'],
                apellido=row['apellido'],
                grupo=row['grupo'],
            )
            alumno_item.save()

        return redirect('/alumno')

    return render(request, 'tu_template_excel.html')

def borrar_todos_los_alumnos(request):
    if request.method == 'GET':
        Alumno.objects.all().delete()
        return redirect('/alumno')

    return HttpResponse("Solicitud no válida.")

def libros_pest(request):
    query = request.GET.get('q')
    if query:
        libros = Libro.objects.filter(Q(codigolibro__icontains=query) | Q(titulo__icontains=query) | Q(autor__icontains=query) | Q(editorial__icontains=query))
    else:
        libros = Libro.objects.all()

    return render(request, "libros.html", context={"current_tab": "libro", "libros": libros})

def agregar_libros(request):
    if request.method == 'POST':
        fechapubl_str = request.POST.get('fechapubl', '')
        if fechapubl_str:
            try:
                fechapubl = int(fechapubl_str)
            except ValueError:
                raise ValidationError('Invalid integer format for fechapublicacion. Please enter a valid integer.')
        else:
            fechapubl = None

        libro_item = Libro(
            titulo=request.POST['titulo'],
            autor=request.POST['autor'],
            editorial=request.POST['editorial'],
            numerotomo=request.POST['numtomo'],
            dewy=request.POST['ubicacion'],  # Ahora 'dewy' en lugar de 'ubicacion'
            publicodirigido=request.POST['publico'],
            fechapublicacion=fechapubl,
            caracteristicasespeciales=request.POST['caracteristicas'],
        )
        libro_item.save()
        return redirect('/libro')

def agregar_copia(request):
    if request.method == 'POST':
        # Obtener el código del libro del formulario
        codigolibro = request.POST.get('codigolibro')
        
        # Verificar si el libro con ese código existe en la base de datos
        libro = get_object_or_404(Libro, codigolibro=codigolibro)
        
        # Si el libro existe, crear una instancia de Copia utilizando el libro obtenido
        if libro:
            copia_item = Copia(codigolibro=libro)
            
            # Guardar la instancia de Copia en la base de datos
            copia_item.save()
            
            # Redireccionar a la página de libros
            return redirect('/libro')
        else:
            # Si el libro no existe, puedes mostrar un mensaje de error o redireccionar a una página de error
           return redirect('/libro')
    else:
        # Si la solicitud no es POST, probablemente deberías manejarla de alguna manera
        # Por ejemplo, podrías mostrar un mensaje de error o redirigir a una página de error
        return redirect('/')


def libro_detalle(request, codigolibro):
    libro_obj = get_object_or_404(Libro, codigolibro=codigolibro)
    return render(request, 'libros_detalle.html', {'libro': libro_obj})

def editar_libro(request, codigolibro):
    libro_obj = get_object_or_404(Libro, codigolibro=codigolibro)

    if request.method == 'POST':
        # Procesa el formulario de edición aquí
        libro_obj.titulo = request.POST['titulo']
        libro_obj.autor = request.POST['autor']
        libro_obj.ilustrador = request.POST['ilustrador']
        libro_obj.editorial = request.POST['editorial']
        libro_obj.numerotomo = request.POST['numerotomo']
        libro_obj.caracteristicasespeciales = request.POST['caracteristicasespeciales']
        libro_obj.dewy = request.POST['ubicacionbiblio']
        libro_obj.publicodirigido = request.POST['publicodirigido']
        try:
            fechapublicacion = int(request.POST['fechapublicacion'])
            libro_obj.fechapublicacion = fechapublicacion
        except ValueError:
            return HttpResponse("Invalid integer format for fechapublicacion. Please enter a valid integer.")
        libro_obj.save()
        return redirect('/libro')

def eliminar_libro(request, codigolibro):
    libro_obj = get_object_or_404(Libro, codigolibro=codigolibro)
    if request.method == 'POST':
        libro_obj.delete()
        return redirect('/libro')
    return render(request, 'eliminar_libro.html', {'libro': libro_obj})

def cargar_desde_excel_libro(request):
    if request.method == 'POST':
        if 'excel_file' in request.FILES:
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file)
            required_columns = ['codigolibro', 'titulo', 'autor', 'editorial']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                missing_columns_str = ', '.join(missing_columns)
                return HttpResponse(f"El archivo Excel no tiene las columnas obligatorias: {missing_columns_str}.")
            for index, row in df.iterrows():
                if any(pd.isna(row[col]) for col in required_columns):
                    return HttpResponse("Los campos obligatorios no pueden estar vacíos.")
                fechapublicacion = row.get('fechapublicacion', datetime.now().date())
                libro_item = Libro(
                    codigolibro=row['codigolibro'],
                    titulo=row['titulo'],
                    autor=row['autor'],
                    editorial=row['editorial'],
                    ilustrador=row.get('ilustrador', ''),
                    fechapublicacion=fechapublicacion,
                    numerotomo=row.get('tomo', ''),
                    caracteristicasespeciales=row.get('caracteristicas', ''),
                    dewy=row.get('ubicacionbiblio', ''),  # Ajustar según sea necesario
                    publicodirigido=row.get('publico', ''),
                )
                libro_item.save()
            return redirect('/libro')
    return render(request, 'tu_template_excel.html')

def borrar_todos_los_libros(request):
    if request.method == 'GET':
        Libro.objects.all().delete()
        return redirect('/libro')
    return HttpResponse("Solicitud no válida.")

def eliminar_libros_por_titulo(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo', None)
        if titulo:
            Libro.objects.filter(titulo=titulo).delete()
    return redirect('/libro')
    
def busqueda_pest(request):
    query = request.GET.get('q')
    if query:
        libros = Libro.objects.filter(Q(codigolibro__icontains=query) | Q(titulo__icontains=query)|Q(autor__icontains=query) |Q(editorial__icontains=query)|Q(ilustrador__icontains=query) )
    else:
        # Si no hay búsqueda, muestra todos los libros
        libros = Libro.objects.all()

    return render(request,"busqueda.html",context={"current_tab": "busqueda", "libros": libros})
def busqeda_detalle(request, codigolibro):
    # Usamos get_object_or_404 para obtener el objeto alumno o retornar un error 404 si no se encuentra
    libro_obj = get_object_or_404(Libro, codigolibro=codigolibro)
    
    return render(request, 'busquedadetalle.html', {'libro': libro_obj})
