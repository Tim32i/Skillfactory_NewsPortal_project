from django.apps import AppConfig


class NewsportalAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'NewsPortal_app'

    def ready(self):
        from . import signals
