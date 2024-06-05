from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver


class Alumno(models.Model):
    clave = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    grupo = models.IntegerField()
    clase = models.CharField(max_length=10, null=True, blank=True)
    sacalibro = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre} {self.apellido} "


class Libro(models.Model):
    codigolibro = models.AutoField(primary_key=True)  # Autogenerar un entero para el código del libro
    titulo = models.CharField(max_length=128)
    autor = models.CharField(max_length=240)
    ilustrador = models.CharField(max_length=100, null=True, blank=True)
    fechapublicacion = models.IntegerField(null=True, blank=True)
    editorial = models.CharField(max_length=100)
    numerotomo = models.CharField(max_length=100, null=True, blank=True)
    caracteristicasespeciales = models.TextField(null=True, blank=True)
    dewy = models.CharField(max_length=45, null=True, blank=True)  # Cambio de nombre a 'dewy'
    item = models.CharField(max_length=45, null=True, blank=True)  # Cambio de nombre a 'dewy'
    publicodirigido = models.CharField(max_length=45, null=True, blank=True)
    palabrasclave = models.TextField(null=True, blank=True)


    def __str__(self):
        return f"{self.codigolibro} - {self.titulo}"  # Cambio en la representación como cadena

class Prestamo(models.Model):
    clave_alumno = models.ForeignKey('Alumno', on_delete=models.CASCADE)  
    clave_copia = models.ForeignKey('Copia', on_delete=models.CASCADE)  
    activo = models.BooleanField(default=True)
    regreso = models.DateField(null=True)  # Campo que acepta fecha (día, mes y año)
    fecha_regreso = models.DateField(null=True,blank=True)  # Campo que acepta fecha (día, mes y año)
    fecha_creacion = models.DateField(null=True,blank=True) # Capo de la fecha que se crea el prestamo

    def __str__(self):
        return f"Prestamo de {self.clave_copia} a {self.clave_alumno}"

class Multa(models.Model):
    monto = models.FloatField()  # Campo de tipo double
    alumno = models.ForeignKey('Alumno', on_delete=models.CASCADE, null=True)  # Campo de referencia a Alumno
    pagado = models.BooleanField(default=False)  # Campo booleano (True/False)
    actualiz= models.DateField(null=True,blank=True)

    def __str__(self):
        return f"Multa de {self.monto} para {self.alumno}"

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

class LastUpdate(models.Model):
    timestamp = models.DateTimeField(auto_now=True)

    @staticmethod
    def get_solo():
        if not LastUpdate.objects.exists():
            LastUpdate.objects.create()
        return LastUpdate.objects.first()

    def __str__(self):
        return f"Last update at {self.timestamp}"