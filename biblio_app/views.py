from django.shortcuts import render
from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import render, redirect
#register your models here

# Create your views here.
def home(request):
    return render(request,"index.html",context={"current_tab": "Inicio"})

def save_student(request):
    student_name = request.POST['nombre_estudiante']
    return render(request,"bienvenida.html",context={'student_name':student_name})