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
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.http import JsonResponse

#register your models here

# Create your views here.
def inicio(request):
    return render(request,"inicio.html",context={"current_tab": "inicio"})
def prestamos(request):
    query = request.GET.get('q')
    if query:
        # Verificar si la consulta es un número puro
        if query.isdigit():
            # Eliminar los ceros a la izquierda en el caso de que existan
            query = str(int(query))
        
        # Realizar la búsqueda utilizando el campo 'clave alumno o clave copia'
        prestamo = Prestamo.objects.filter(
            Q(clave_alumno__icontains=query) |
            Q(clave_copia__icontains=query)
        ).distinct().order_by('-pk')
    else:
        # Si no hay búsqueda, mostrar todos los prestamos
        prestamo = Prestamo.objects.all().order_by('-pk')

    # Devolver una respuesta con la lista de prestamos
    return render(request,"prestamo.html",context={"current_tab": "prestamo", "prestamo": prestamo})

def retornos(request):
    return render(request,"retorno.html",context={"current_tab": "retorno"})
def multas(request):
    return render(request,"multas.html",context={"current_tab": "multa"})
def etiquetas(request):
    return render(request,"etiqueta.html",context={"current_tab": "etiqueta"})
def credenciales(request):
    return render(request,"credencial.html",context={"current_tab": "credecial"})

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
        # Verificar si la consulta es un número puro
        if query.isdigit():
            # Eliminar los ceros a la izquierda en el caso de que existan
            query = str(int(query))
        
        # Realizar la búsqueda utilizando el campo 'nombre', 'apellido', 'clave' o 'grupo'
        alumnos = Alumno.objects.filter(
            Q(nombre__icontains=query) |
            Q(apellido__icontains=query) |
            Q(nombre__icontains=query.split()[0]) &  # Buscar el primer nombre
            Q(apellido__icontains=query.split()[-1]) |  # Buscar el último apellido
            Q(clave__icontains=query) |
            Q(grupo__icontains=query)
        ).distinct()
    else:
        # Si no hay búsqueda, mostrar todos los alumnos
        alumnos = Alumno.objects.all()

    # Devolver una respuesta con la lista de alumnos encontrados
    return render(request, 'alumnos.html', {"current_tab": "alumno", "alumnos": alumnos})


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
            if 'clave' in df.columns and not pd.isna(row['clave']):
                clave = row['clave']
            else:
                clave = None  # Asignar None para que se autoasigne la clave por el sistema

            alumno_item = Alumno(
                clave=clave,
                nombre=row['nombre'],
                apellido=row['apellido'],
                grupo=row['grupo'],
            )
            alumno_item.save()

        return redirect('/alumno')

    return render(request, 'tu_template_excel.html')

def borrar_todos_los_alumnos(request):
    try:
        # Eliminar todos los alumnos con un valor de grupo de 6 o superior
        Alumno.objects.filter(grupo__gte=6).delete()
        
        # Modificar todos los datos en la tabla de alumnos sumando uno al valor de grupo
        Alumno.objects.all().update(grupo=models.F('grupo') + 1)
        
        # Redireccionar a la página de alumnos
        return redirect('/alumno')  # Cambia 'alumnos' por la URL de la página de alumnos en tu proyecto
    
    except ValidationError as e:
        # Si se produce una excepción de validación, mostrar un mensaje de error
        return render(request, 'error.html', {'mensaje': '; '.join(e.messages)})

def libros_pest(request):
    query = request.GET.get('q')
    if query:
        # Verificar si la consulta es un número puro
        if query.isdigit():
            # Eliminar los ceros a la izquierda en el caso de que existan
            query = str(int(query))

        libros = Libro.objects.filter(
            Q(codigolibro__icontains=query) |
            Q(titulo__icontains=query) |
            Q(autor__icontains=query) |
            Q(editorial__icontains=query)
        )
    else:
        libros = Libro.objects.all()

    return render(request, "libros.html", context={"current_tab": "libro", "libros": libros})


def agregar_libros(request):
    if request.method == 'POST':
        try:
            fechapubl_str = request.POST.get('fechapubl', '')
            if fechapubl_str:
                fechapubl = int(fechapubl_str)
            else:
                fechapubl = None

            libro_item = Libro(
                titulo=request.POST.get('titulo', ''),
                autor=request.POST.get('autor', ''),
                editorial=request.POST.get('editorial', ''),
                numerotomo=request.POST.get('numtomo', ''),
                dewy=request.POST.get('ubicacion', ''),  # Ahora 'dewy' en lugar de 'ubicacion'
                publicodirigido=request.POST.get('publico', ''),
                fechapublicacion=fechapubl,
                caracteristicasespeciales=request.POST.get('caracteristicas', ''),
                ilustrador=request.POST.get('ilustrador','')
            )
            libro_item.full_clean()  # Realiza todas las validaciones del modelo
            libro_item.save()
            return redirect('/libro')
        
        except ValidationError as e:
            # Si se produce una excepción de validación, mostrar un mensaje de error
            return render(request, 'error.html', {'mensaje': '; '.join(e.messages)})

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
           return render(request, 'error.html', {'mensaje': 'El codigo de libro introducido no corresoponde an ningun libro en la base favor de verificarlo'})
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
        libro_obj.editorial = request.POST['editorial']

        # Los campos no obligatorios se manejan si están presentes en la solicitud POST
        libro_obj.ilustrador = request.POST.get('ilustrador', None)
        libro_obj.numerotomo = request.POST.get('numerotomo', None)
        libro_obj.caracteristicasespeciales = request.POST.get('caracteristicasespeciales', None)
        libro_obj.dewy = request.POST.get('ubicacionbiblio', None)
        libro_obj.publicodirigido = request.POST.get('publicodirigido', None)

        # Obtener el valor de fechapublicacion del formulario
        fechapublicacion = request.POST.get('fechapublicacion')

        # Si el valor obtenido es None o vacío, establecer fechapublicacion como None
        if not fechapublicacion:
            libro_obj.fechapublicacion = None
        else:
            try:
                # Intentar convertir el valor a un entero
                fechapublicacion = int(fechapublicacion)
                libro_obj.fechapublicacion = fechapublicacion
            except ValueError:
                return HttpResponse("Invalid integer format for fechapublicacion. Please enter a valid integer.")

        libro_obj.save()
        return redirect('/libro')

    # Si la solicitud no es POST, renderiza el formulario de edición
    return render(request, 'editar_libro.html', {'libro': libro_obj})



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
            required_columns = ['titulo', 'autor', 'editorial']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                missing_columns_str = ', '.join(missing_columns)
                return HttpResponse(f"El archivo Excel no tiene las columnas obligatorias: {missing_columns_str}.")
            for index, row in df.iterrows():
                if any(pd.isna(row[col]) for col in required_columns):
                    return HttpResponse("Los campos obligatorios no pueden estar vacíos.")
                if 'codigolibro' in df.columns and pd.notna(row['codigolibro']):
                    codigolibro = row['codigolibro']
                else:
                    codigolibro = None
                fechapublicacion = int(row.get('fechapublicacion', None))  # Cambiar a entero
                libro_item = Libro(
                    codigolibro=codigolibro,
                    titulo=row['titulo'],
                    autor=row['autor'],
                    editorial=row['editorial'],
                    ilustrador=row.get('ilustrador', None),
                    fechapublicacion=fechapublicacion,
                    numerotomo=row.get('tomo', None),
                    caracteristicasespeciales=row.get('caracteristicas', None),
                    dewy=row.get('ubicacionbiblio', None),
                    publicodirigido=row.get('publico', None),
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
        # Verificar si la consulta es un número puro
        if query.isdigit():
            # Eliminar los ceros a la izquierda en el caso de que existan
            query = str(int(query))
    if query:
        copias = Copia.objects.filter(Q(clavecopia__icontains=query) | Q(codigolibro__titulo__icontains=query) | Q(codigolibro__autor__icontains=query) | Q(codigolibro__editorial__icontains=query) | Q(codigolibro__ilustrador__icontains=query))
    else:
        # Si no hay búsqueda, muestra todas las copias
        copias = Copia.objects.all()

    return render(request,"busqueda.html",context={"current_tab": "busqueda", "copias": copias})

def busqeda_detalle(request, clavecopia):
    # Usamos get_object_or_404 para obtener el objeto alumno o retornar un error 404 si no se encuentra
    copia_obj = get_object_or_404(Copia, clavecopia=clavecopia)
    
    return render(request, 'busquedadetalle.html', {'copia': copia_obj})

def cargar_copias_desde_excel(request):
    if request.method == 'POST':
        if 'excel_file' in request.FILES:
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file)

            required_columns = ['codigolibro']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                missing_columns_str = ', '.join(missing_columns)
                return HttpResponse(f"El archivo Excel no tiene las columnas necesarias: {missing_columns_str}.")

            for index, row in df.iterrows():
                codigolibro = row['codigolibro']

                if 'clavecopia' in df.columns and not pd.isna(row['clavecopia']):
                    clavecopia = row['clavecopia']
                else:
                    clavecopia = None  # Asignar None para que se autoasigne la clave de copia por Django

                libro_existente = Libro.objects.filter(codigolibro=codigolibro).first()
                if libro_existente:
                    copia_item = Copia(
                        clavecopia=clavecopia,
                        codigolibro=libro_existente,
                        disponible=True,  # Asignar True por defecto
                        clavealumno=None,  # Asignar None por defecto
                    )
                    copia_item.save()
                else:
                    return HttpResponse(f"No se encontró el libro con la clave: {codigolibro}")

            return redirect('/libro')  # Redirigir a la página de copias después de cargar las copias

    return render(request, 'tu_template_excel.html')

def eliminar_copia(request, pk):
    copia_obj = get_object_or_404(Copia, clavecopia=pk)
    print(copia_obj)

    if request.method == 'POST':
        copia_obj.delete()
        return redirect('/busqueda')

    return redirect('/busqueda')

def nuevo_prestamo(request):
    if request.method == 'POST':
        clave_alumno = request.POST.get('clave_alumno')
        clave_copia = request.POST.get('clave_copia')

        if not (clave_alumno and clave_copia):
            return render(request, 'error.html', {'mensaje': 'Por favor, completa todos los campos obligatorios.'})
        
        if clave_alumno.isdigit():
        # Eliminar los ceros a la izquierda en el caso de que existan
            clave_alumno = str(int(clave_alumno))
        if clave_copia.isdigit():
        # Eliminar los ceros a la izquierda en el caso de que existan
            clave_copia = str(int(clave_copia))
        try:
            alumno = Alumno.objects.get(clave=clave_alumno)
            copia = Copia.objects.get( clavecopia=clave_copia)

            if not alumno.sacalibro and copia.disponible:
                prestamo = Prestamo.objects.create(
                    clave_alumno=alumno,
                    clave_copia=copia,
                    activo=True,
                    regreso=datetime.now() + timedelta(days=7),
                    fecha_regreso=None
                )

                # Modificar disponibilidad de copia y clave de alumno en la copia
                copia.disponible = False
                copia.clavealumno = alumno
                copia.save()

                # Actualizar estado de sacalibro en alumno
                alumno.sacalibro = True
                alumno.save()

                return redirect('/prestamo')
            else:
                return render(request, 'error.html', {'mensaje': 'El alumno ya tiene un libro sacado o la copia no está disponible.'})
        except (Alumno.DoesNotExist, Copia.DoesNotExist):
            return render(request, 'error.html', {'mensaje': 'La clave de alumno o de copia no son válidas.'})

    return render(request, 'error.html', {'mensaje': 'El método de solicitud no es válido.'})