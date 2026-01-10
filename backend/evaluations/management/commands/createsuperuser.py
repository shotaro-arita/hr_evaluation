from django.contrib.auth.management.commands.createsuperuser import (
    Command as BaseCommand,
)
from django.core.management import CommandError
from evaluations.models.employee import DbEmployee


class Command(BaseCommand):
    # コマンド
    # python manage.py createsuperuser --employee_code XXXXX
    def add_arguments(self, parser) -> None:
        super().add_arguments(parser)
        parser.add_argument("--employee-code", dest="employee_code")

    def handle(self, *args, **options) -> None:
        employee_code = options.get("employee_code") or self.get_input_data(
            self.UserModel._meta.get_field("employee_code"),
            "employee_code",
            "Employee code: ",
            options.get("stdin"),
        )
        try:
            employee = DbEmployee.objects.get(employee_code=employee_code)
        except DbEmployee.DoesNotExist as exc:
            raise CommandError(f"Employee not found: {employee_code}") from exc

        options["employee"] = employee
        super().handle(*args, **options)
