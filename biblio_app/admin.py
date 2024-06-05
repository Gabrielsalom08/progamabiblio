from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Alumno)
admin.site.register(Libro)
admin.site.register(Copia)
admin.site.register(Multa)
admin.site.register(Prestamo)
admin.site.register(LastUpdate)