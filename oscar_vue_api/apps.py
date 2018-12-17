from django.apps import AppConfig


class OscarVueApiConfig(AppConfig):
    name = 'oscar_vue_api'
    def ready(self):
        import oscar_vue_api.signals
