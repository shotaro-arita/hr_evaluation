import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from evaluations.models.employee import DbEmployee
from evaluations.models.evaluation_assignment import DbEvaluationAssignment


class Command(BaseCommand):
    # python manage.py import_evaluation_assignment evaluations/fixtures/evaluation_assignment_sample.json
    help = "Import evaluation assignments from a JSON file."

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

        assignments = data.get("evaluation_assignments")
        if not isinstance(assignments, list):
            raise CommandError("JSON must include an 'evaluation_assignments' list.")

        required_keys = {
            "uuid",
            "target_employee_code",
            "manager_employee_code",
            "role",
        }
        for index, assignment in enumerate(assignments):
            if not isinstance(assignment, dict):
                raise CommandError(f"Assignment at index {index} must be an object.")
            missing_keys = required_keys - assignment.keys()
            if missing_keys:
                missing = ", ".join(sorted(missing_keys))
                raise CommandError(
                    f"Assignment at index {index} missing keys: {missing}"
                )

            try:
                target_employee = DbEmployee.objects.get(
                    employee_code=assignment["target_employee_code"]
                )
            except DbEmployee.DoesNotExist as exc:
                raise CommandError(
                    f"Target employee not found: {assignment['target_employee_code']}"
                ) from exc

            try:
                manager_employee = DbEmployee.objects.get(
                    employee_code=assignment["manager_employee_code"]
                )
            except DbEmployee.DoesNotExist as exc:
                raise CommandError(
                    f"Manager employee not found: {assignment['manager_employee_code']}"
                ) from exc

            DbEvaluationAssignment.objects.update_or_create(
                uuid=assignment["uuid"],
                defaults={
                    "target_employee": target_employee,
                    "manager_employee": manager_employee,
                    "role": assignment["role"],
                },
            )

        self.stdout.write(self.style.SUCCESS("Evaluation assignment import completed."))
