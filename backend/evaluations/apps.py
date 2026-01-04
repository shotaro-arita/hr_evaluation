import inject
from django.apps import AppConfig
from config.inject_config import injection_config


class EvaluationsConfig(AppConfig):
    name = "evaluations"

    def ready(self):
        inject.configure_once(injection_config)