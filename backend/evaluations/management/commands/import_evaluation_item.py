import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from evaluations.models.evaluation_item import DbEvaluationItem


class Command(BaseCommand):
    # python manage.py import_evaluation_item evaluations/fixtures/evaluation_item_sample.json
    help = "Import evaluation items from a JSON file."

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

        items = data.get("evaluation_items")
        if not isinstance(items, list):
            raise CommandError("JSON must include an 'evaluation_items' list.")

        required_keys = {
            "uuid",
            "title",
            "category",
            "description",
            "criteria_1",
            "criteria_2",
            "criteria_3",
            "criteria_4",
            "criteria_5",
        }
        for index, item in enumerate(items):
            if not isinstance(item, dict):
                raise CommandError(f"Item at index {index} must be an object.")
            missing_keys = required_keys - item.keys()
            if missing_keys:
                missing = ", ".join(sorted(missing_keys))
                raise CommandError(f"Item at index {index} missing keys: {missing}")

            DbEvaluationItem.objects.update_or_create(
                uuid=item["uuid"],
                defaults={
                    "title": item["title"],
                    "category": item["category"],
                    "description": item["description"],
                    "criteria_1": item["criteria_1"],
                    "criteria_2": item["criteria_2"],
                    "criteria_3": item["criteria_3"],
                    "criteria_4": item["criteria_4"],
                    "criteria_5": item["criteria_5"],
                },
            )

        self.stdout.write(self.style.SUCCESS("Evaluation item import completed."))
