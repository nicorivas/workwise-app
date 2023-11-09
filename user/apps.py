from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'

    def ready(self):
        # Implicitly connect signal handlers decorated with @receiver.
        import user.signals.handlers

        ## Explicitly connect a signal handler.
        #request_finished.connect(signals.my_callback)