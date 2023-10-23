from django.apps import AppConfig


class SmartmecanicoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'smartmecanico'

    def ready(self):
        import smartmecanico.signals
