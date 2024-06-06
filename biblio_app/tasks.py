# tasks.py
import os
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.db import connection
from django.utils import timezone

class TaskSingleton:
    _instance = None
    _is_running = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if TaskSingleton._is_running:
            print("TaskSingleton instance is already running. Initialization aborted.")  # Debugging
            return

        print("Creating TaskSingleton instance")  # Debugging
        self.scheduler = BackgroundScheduler()

        # Task to update multas
        multas_trigger = CronTrigger(day_of_week='mon-fri', hour=8, minute='30-59')
        self.scheduler.add_job(self.actualizar_multas, trigger=multas_trigger, misfire_grace_time=3600, max_instances=1)
        print("Scheduler added job for actualizar_multas")  # Debugging

        # Task to update the database every hour
        update_trigger = CronTrigger(minute='0-5')  # Runs every hour
        self.scheduler.add_job(self.update_last_update, trigger=update_trigger, misfire_grace_time=3600, max_instances=1)
        print("Scheduler added job for update_last_update")  # Debugging

        self.scheduler.start()
        print("Scheduler started")  # Debugging

        TaskSingleton._is_running = True
        atexit.register(self._cleanup)

    def _cleanup(self):
        if 'TASK_SINGLETON_INITIALIZED' in os.environ:
            del os.environ['TASK_SINGLETON_INITIALIZED']

    def actualizar_multas(self):
        self.ensure_db_connection()
        print("Executing actualizar_multas")  # Debugging
        from .models import Prestamo, Multa
        prestamos_activos = Prestamo.objects.filter(activo=True, regreso__lt=timezone.now().date())
        print("Total active loans:", prestamos_activos.count())  # Debugging
        for prestamo in prestamos_activos:
            print("Processing loan:", prestamo.id)  # Debugging
            multas = Multa.objects.filter(alumno=prestamo.clave_alumno)
            if multas.exists():
                for multa in multas:
                    if multa.actualiz != timezone.now().date():
                        multa.monto += 2
                        multa.actualiz = timezone.now().date()
                        multa.save()
            else:
                Multa.objects.create(monto=2, alumno=prestamo.clave_alumno, actualiz=timezone.now().date())

    def update_last_update(self):
        self.ensure_db_connection()
        print("Executing update_last_update")  # Debugging
        from .models import LastUpdate
        last_update = LastUpdate.get_solo()
        last_update.timestamp = timezone.now()
        last_update.save()
        print("Updated LastUpdate timestamp")  # Debugging

    def ensure_db_connection(self):
        if connection.connection and not connection.is_usable():
            print("Database connection was not usable, closing and reconnecting.")  # Debugging
            connection.close()
        connection.ensure_connection()

def initialize_task_singleton():
    TaskSingleton()
