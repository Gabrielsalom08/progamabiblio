"""
URL configuration for biblio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', inicio),
    path('inicio', inicio),  # Asegúrate de agregar la barra al final para ser consistente
    path('libro', libros_pest),
    path('credencial', credenciales),
    path('busqueda', busqueda_pest),
    path('nuevoprestamo', nuevo_prestamo),
    path('prestamo', prestamos),
    path('retorno', retornos),
    path('multa', multas),
    path('etiqueta', etiquetas),
    path('alumno', alumno_pest),
    path('', include("django.contrib.auth.urls")),
    path('copia/eliminar/<int:pk>/', eliminar_copia, name='eliminar_copia'),
    path('alumno/agregar', agregar_alum),
    path('alumno/<int:pk>', alumno_detalle, name='alumno_detalle'),
    path('alumno/editar/<int:pk>', editar_alumno, name='editar_alumno'),
    path('alumno/eliminar/<int:pk>/', eliminar_alumno, name='eliminar_alumno'),
    path('alumno/cargar_excel', cargar_desde_excel, name='cargar_desde_excel'),
    path('alumno/borrar_todos', borrar_todos_los_alumnos, name='borrar_todos_los_alumnos'),
    path('libro/eliminar_por_titulo', eliminar_libros_por_titulo, name='eliminar_libros_por_titulo'),
    path('libro/agregar/', agregar_libros),
    path('busqueda/<int:clavecopia>', busqeda_detalle, name='busqueda_detalle'),
    path('libro/cargar_excel_copia', cargar_copias_desde_excel, name='cargar_desde_excel_copias'),
    path('libro/agregar-copia/', agregar_copia, name='agregar_copia'),
    path('libro/<int:codigolibro>', libro_detalle, name='libro_detalle'),
    path('libro/editar/<int:codigolibro>', editar_libro, name='editar_libro'),
    path('libro/eliminar/<int:codigolibro>', eliminar_libro, name='eliminar_libro'),
    path('libro/cargar_excel', cargar_desde_excel_libro, name='cargar_desde_excel_libros'),
    path('libro/borrar_todos', borrar_todos_los_libros, name='borrar_todos_los_libros'),
    path('libro/eliminar_por_titulo', eliminar_libros_por_titulo, name='eliminar_libros_por_titulo'),

]

