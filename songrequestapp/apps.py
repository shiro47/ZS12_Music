from django.apps import AppConfig
import os

class SongrequestappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'songrequestapp'
    
    def ready(self):
        from . import BackgroundTasks

        if os.environ.get('RUN_MAIN', None) != 'true':
            BackgroundTasks.start_scheduler()