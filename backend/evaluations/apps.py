import inject
from django.apps import AppConfig


class EvaluationsConfig(AppConfig):
    name = "evaluations"

    def ready(self):
        from config.inject_config import injection_config

        inject.configure_once(injection_config)
