# apps.py

from django.apps import AppConfig
from .tasks import TaskSingleton  # Import TaskSingleton

class BiblioAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'biblio_app'

    def ready(self):
        TaskSingleton()  # Create and initialize an instance of TaskSingleton
