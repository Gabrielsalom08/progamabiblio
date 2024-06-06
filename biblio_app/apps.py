# apps.py
from django.apps import AppConfig

class BiblioAppConfig(AppConfig):
    name = 'biblio_app'

    def ready(self):
        from .tasks import initialize_task_singleton
        initialize_task_singleton()
