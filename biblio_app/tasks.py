from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.utils import timezone
from datetime import datetime

class TaskSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        print("Creating TaskSingleton instance")  # Add this line for debugging
        self.scheduler = BackgroundScheduler()
        
        # Define the trigger to run at any time between 6:30 am and 7:00 am every weekday
        trigger = CronTrigger(day_of_week='mon-fri', hour=13, minute='10-59')
        
        self.scheduler.add_job(self.actualizar_multas, trigger=trigger, misfire_grace_time=3600, max_instances=1)
        print("Scheduler added job")  # Add this line for debugging
        self.scheduler.start()
        print("Scheduler started")  # Add this line for debugging

    def actualizar_multas(self):
        print("Executing actualizar_multas")  # Add this line for debugging
        # Import models locally to avoid AppRegistryNotReady error
        from .models import Prestamo, Multa

        prestamos_activos = Prestamo.objects.filter(activo=True, regreso__lt=timezone.now().date())
        print("Total active loans:", prestamos_activos.count())  # Add this line for debugging
        for prestamo in prestamos_activos:
            print("Processing loan:", prestamo.id)  # Add this line for debugging
            multas = Multa.objects.filter(prestamo=prestamo)
            if multas.exists():
                for multa in multas:
                    if multa.actualiz != timezone.now().date():
                        multa.monto += 2
                        multa.actualiz = timezone.now().date()
                        multa.save()
            else:
                Multa.objects.create(monto=2, alumno=prestamo.clave_alumno, prestamo=prestamo, actualiz=timezone.now().date())
