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

class libro(models.Model):
    def __str__(self):
        nombre= self.codigolibro+' '+self.titulo 
        return nombre
    codigolibro = models.CharField(max_length=45, primary_key=True)
    titulo = models.CharField(max_length=128)
    autor = models.CharField(max_length=100)
    ilustrador = models.CharField(max_length=100, null=True, blank=True)
    fechapublicacion = models.DateField(null=True, blank=True)
    editorial = models.CharField(max_length=100)
    numerotomo = models.CharField(max_length=100, null=True, blank=True)
    caracteristicasespeciales = models.TextField(null=True, blank=True)
    disponible = models.BooleanField(default=True)
    ubicacionbiblio = models.CharField(max_length=45, null=True, blank=True)
    publicodirigido = models.CharField(max_length=45, null=True, blank=True)
    