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
    path('',inicio),
    path('inicio', inicio),
    path('libro', libros),
    path('busqueda', busquedas),
    path('prestamo', prestamos),
    path('retorno', retornos),
    path('multa', multas),
    path('etiqueta', etiquetas),
    path('alumno', alumno_pest),
    path('',include("django.contrib.auth.urls")),
    path('alumno/agregar',agregar_alum),
    path('alumno/<int:pk>/', alumno_detalle, name='alumno_detalle'),
    path('alumno/editar/<int:pk>/', editar_alumno, name='editar_alumno'),
    path('alumno/eliminar/<int:pk>/', eliminar_alumno, name='eliminar_alumno'),
    path('alumno/cargar_excel', cargar_desde_excel, name='cargar_desde_excel'),
    path('alumno/borrar_todos', borrar_todos_los_alumnos, name='borrar_todos_los_alumnos'),

]

