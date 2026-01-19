import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from evaluations.models.employee import DbEmployee
from evaluations.models.user import DbUser


class Command(BaseCommand):
    # コマンド
    # python manage.py import_user /app/evaluations/fixtures/user_sample.json
    help = "Import users from a JSON file."

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

        users = data.get("users")
        if not isinstance(users, list):
            raise CommandError("JSON must include a 'users' list.")

        required_keys = {"uuid", "employee_code", "password", "name"}
        for index, user in enumerate(users):
            if not isinstance(user, dict):
                raise CommandError(f"User at index {index} must be an object.")
            missing_keys = required_keys - user.keys()
            if missing_keys:
                missing = ", ".join(sorted(missing_keys))
                raise CommandError(f"User at index {index} missing keys: {missing}")

            try:
                employee = DbEmployee.objects.get(employee_code=user["employee_code"])
            except DbEmployee.DoesNotExist as exc:
                raise CommandError(
                    f"Employee not found: {user['employee_code']}"
                ) from exc

            db_user, _created = DbUser.objects.update_or_create(
                uuid=user["uuid"],
                defaults={
                    "employee_code": user["employee_code"],
                    "employee": employee,
                    "name": user["name"],
                    "is_active": user.get("is_active", True),
                    "is_staff": user.get("is_staff", False),
                },
            )
            db_user.set_password(user["password"])
            db_user.save(update_fields=["password"])

        self.stdout.write(self.style.SUCCESS("User import completed."))
