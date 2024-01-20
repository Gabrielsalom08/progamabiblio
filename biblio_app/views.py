from django.shortcuts import render
from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import render, redirect
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
