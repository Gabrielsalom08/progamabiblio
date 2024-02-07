from django.apps import AppConfig

class BiblioAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'biblio_app'

    def ready(self):
        from .tasks import iniciar_planificador
        iniciar_planificador()
