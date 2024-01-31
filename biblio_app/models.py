from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver


class Alumno(models.Model):
    clave = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    grupo = models.IntegerField()
    sacalibro = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre} {self.apellido} "


class Libro(models.Model):
    codigolibro = models.AutoField(primary_key=True)  # Autogenerar un entero para el código del libro
    titulo = models.CharField(max_length=128)
    autor = models.CharField(max_length=100)
    ilustrador = models.CharField(max_length=100, null=True, blank=True)
    fechapublicacion = models.IntegerField(null=True, blank=True)
    editorial = models.CharField(max_length=100)
    numerotomo = models.CharField(max_length=100, null=True, blank=True)
    caracteristicasespeciales = models.TextField(null=True, blank=True)
    dewy = models.CharField(max_length=45, null=True, blank=True)  # Cambio de nombre a 'dewy'
    publicodirigido = models.CharField(max_length=45, null=True, blank=True)

    def __str__(self):
        return f"{self.codigolibro} - {self.titulo}"  # Cambio en la representación como cadena

class Copia(models.Model):
    clavecopia = models.AutoField(primary_key=True)  # Autogenerar un entero para la clave de copia
    codigolibro = models.ForeignKey(Libro, on_delete=models.CASCADE)  # Llave foránea de Libro
    disponible = models.BooleanField(default=True)
    clavealumno = models.ForeignKey('Alumno', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Copia {self.clavecopia} de {self.codigolibro.titulo}"

@receiver(pre_delete, sender=Libro)
def eliminar_copias_asociadas(sender, instance, **kwargs):
    Copia.objects.filter(codigolibro=instance).delete()