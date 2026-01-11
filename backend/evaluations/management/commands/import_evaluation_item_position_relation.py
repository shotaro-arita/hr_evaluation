import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from evaluations.models.evaluation_item_position_relation import (
    DbEvaluationItemPositionRelation,
)


class Command(BaseCommand):
    # python manage.py import_evaluation_item_position_relation evaluations/fixtures/evaluation_item_position_relation_sample.json
    help = "Import evaluation item position relations from a JSON file."

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

        relations = data.get("evaluation_item_position_relations")
        if not isinstance(relations, list):
            raise CommandError(
                "JSON must include an 'evaluation_item_position_relations' list."
            )

        required_keys = {"uuid", "position", "evaluation_item_uuid", "order"}
        for index, relation in enumerate(relations):
            if not isinstance(relation, dict):
                raise CommandError(f"Relation at index {index} must be an object.")
            missing_keys = required_keys - relation.keys()
            if missing_keys:
                missing = ", ".join(sorted(missing_keys))
                raise CommandError(f"Relation at index {index} missing keys: {missing}")

            DbEvaluationItemPositionRelation.objects.update_or_create(
                uuid=relation["uuid"],
                defaults={
                    "position": relation["position"],
                    "evaluation_item_id": relation["evaluation_item_uuid"],
                    "order": relation["order"],
                },
            )

        self.stdout.write(
            self.style.SUCCESS("Evaluation item position relation import completed.")
        )
