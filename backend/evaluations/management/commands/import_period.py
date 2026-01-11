import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.dateparse import parse_datetime
from evaluations.models.period import DbPeriod


class Command(BaseCommand):
    # python manage.py import_period evaluations/fixtures/period_sample.json
    help = "Import periods from a JSON file."

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

        periods = data.get("periods")
        if not isinstance(periods, list):
            raise CommandError("JSON must include a 'periods' list.")

        required_keys = {"uuid", "name", "start_date", "end_date"}
        for index, period in enumerate(periods):
            if not isinstance(period, dict):
                raise CommandError(f"Period at index {index} must be an object.")
            missing_keys = required_keys - period.keys()
            if missing_keys:
                missing = ", ".join(sorted(missing_keys))
                raise CommandError(f"Period at index {index} missing keys: {missing}")

            start_date = parse_datetime(period["start_date"])
            if start_date is None:
                raise CommandError(
                    f"Invalid start_date at index {index}: {period['start_date']}"
                )
            end_date = parse_datetime(period["end_date"])
            if end_date is None:
                raise CommandError(
                    f"Invalid end_date at index {index}: {period['end_date']}"
                )

            DbPeriod.objects.update_or_create(
                uuid=period["uuid"],
                defaults={
                    "name": period["name"],
                    "start_date": start_date,
                    "end_date": end_date,
                },
            )

        self.stdout.write(self.style.SUCCESS("Period import completed."))
