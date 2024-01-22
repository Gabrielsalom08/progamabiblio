from django.db import models

# Create your models here.
class alumno (models.Model):
    def __str__(self) :
        name= self.nombre+ ' '+ self.apellido+' '+self.grupo
        return name
    clave=models.CharField(max_length=20)
    nombre=models.CharField(max_length=50)
    apellido=models.CharField(max_length=50)
    grupo=models.CharField(max_length=10)