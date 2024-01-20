from django.db import models

# Create your models here.
class Alumno(models.Model):
    clave = models.CharField(max_length=16, primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    grupo = models.CharField(max_length=5)
    correo = models.CharField(max_length=128, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'Alumnos'

class User(models.Model):
    user = models.CharField(max_length=32, primary_key=True)
    password = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'user'
