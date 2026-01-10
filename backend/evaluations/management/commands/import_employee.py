import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from evaluations.models.employee import DbEmployee


class Command(BaseCommand):
    # コマンド
    # python manage.py import_employee /app/evaluations/fixtures/employee_sample.json
    help = "Import employees from a JSON file."

    def add_arguments(self, parser) -> None:
        parser.add_argument("json_path", type=str)

    @transaction.atomic
    def handle(self, *args, **options) -> None:
        json_path = Path(options["json_path"])
        if not json_path.exists():
            raise CommandError(f"File not found: {json_path}")

        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise CommandError(f"Invalid JSON: {exc}") from exc

        employees = data.get("employees")
        if not isinstance(employees, list):
            raise CommandError("JSON must include an 'employees' list.")

        required_keys = {"uuid", "employee_code", "name", "position", "job_type"}
        for index, employee in enumerate(employees):
            if not isinstance(employee, dict):
                raise CommandError(f"Employee at index {index} must be an object.")
            missing_keys = required_keys - employee.keys()
            if missing_keys:
                missing = ", ".join(sorted(missing_keys))
                raise CommandError(f"Employee at index {index} missing keys: {missing}")

            DbEmployee.objects.update_or_create(
                uuid=employee["uuid"],
                defaults={
                    "employee_code": employee["employee_code"],
                    "name": employee["name"],
                    "position": employee["position"],
                    "job_type": employee["job_type"],
                },
            )

        self.stdout.write(self.style.SUCCESS("Employee import completed."))
