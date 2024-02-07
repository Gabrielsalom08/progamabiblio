# tasks.py

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.utils import timezone
from .models import Prestamo, Multa
import pytz
from datetime import datetime
import time

# Obtener la hora actual en la zona horaria 'America/Mexico_City'
tz = pytz.timezone('America/Mexico_City')
now = datetime.now(tz)
print("Hora actual en 'America/Mexico_City':", now)


# Define la función para actualizar multas
def actualizar_multas():
    time.sleep(2)
    prestamos_activos = Prestamo.objects.filter(activo=True, regreso__lt=timezone.now().date())
    print("hola")
    for prestamo in prestamos_activos:
        multas = Multa.objects.filter(prestamo=prestamo)
        if multas.exists():
            for multa in multas:
                multa.monto += 1
                multa.save()
        else:
            Multa.objects.create(monto=1, alumno=prestamo.clave_alumno, prestamo=prestamo)
    

def iniciar_planificador():
    scheduler = BackgroundScheduler()
    # Configurar la hora y los días de la semana en los que se ejecutará la tarea
    trigger = CronTrigger(hour=19, minute=47, day_of_week='mon-fri')  # Ejemplo: ejecutar a las 6:00 AM de lunes a viernes
    # Agregar la tarea para ejecutar actualizar_multas en la hora y días de la semana especificados
    scheduler.add_job(actualizar_multas, trigger=trigger)
    scheduler.start()

