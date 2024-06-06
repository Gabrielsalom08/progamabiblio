# tasks.py
import os
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.db import connection
from django.utils import timezone
import shutil
import time

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
        multas_trigger = CronTrigger(day_of_week='mon-fri', hour=7, minute='30-59')
        self.scheduler.add_job(self.actualizar_multas, trigger=multas_trigger, misfire_grace_time=3600, max_instances=1)
        

        # Task to update the database every hour
        update_trigger = CronTrigger(minute='0-5')  # Runs every hour
        self.scheduler.add_job(self.update_last_update, trigger=update_trigger, misfire_grace_time=3600, max_instances=1)

        backup_trigger = CronTrigger(day_of_week='mon-fri',  hour=16, minute='0-2')
        self.scheduler.add_job(self.backup_database, trigger=backup_trigger)
        self.scheduler.start()

        print("Scheduler started")  # Debugging

        TaskSingleton._is_running = True
        atexit.register(self._cleanup)

    def _cleanup(self):
        if 'TASK_SINGLETON_INITIALIZED' in os.environ:
            del os.environ['TASK_SINGLETON_INITIALIZED']

    def actualizar_multas(self):
        self.ensure_db_connection()
        from .models import Prestamo, Multa
        prestamos_activos = Prestamo.objects.filter(activo=True, regreso__lt=timezone.now().date())
        for prestamo in prestamos_activos:
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
        from .models import LastUpdate
        last_update = LastUpdate.get_solo()
        last_update.timestamp = timezone.now()
        last_update.save()
        
    def backup_database(self):
        backup_dir = 'backups'
        db_file = 'db.sqlite3'

        # Create the backup directory if it doesn't exist
        os.makedirs(backup_dir, exist_ok=True)

        # Generate backup file name with timestamp
        timestamp = timezone.now().strftime('%Y-%m-%d_%H-%M-%S')
        backup_file = os.path.join(backup_dir, f'backup_{timestamp}.sqlite3')

        # Copy the database file to the backup directory
        shutil.copy2(db_file, backup_file)

        # Delete old backups if there are more than seven
        backups = sorted(os.listdir(backup_dir), key=lambda x: os.path.getmtime(os.path.join(backup_dir, x)))
        if len(backups) > 7:
            for old_backup in backups[:len(backups) - 7]:
                os.remove(os.path.join(backup_dir, old_backup))

        print("Backup completed:", backup_file)
        time.sleep(2.25 * 60)

    def ensure_db_connection(self):
        if connection.connection and not connection.is_usable():
            print("Database connection was not usable, closing and reconnecting.")  # Debugging
            connection.close()
        connection.ensure_connection()
        

def initialize_task_singleton():
    TaskSingleton()
