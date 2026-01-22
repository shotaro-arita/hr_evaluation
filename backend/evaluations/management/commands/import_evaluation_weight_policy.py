import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from evaluations.models.evaluation_weight_policy import DbEvaluationWeightPolicy
from evaluations.models.period import DbPeriod


class Command(BaseCommand):
    # python manage.py import_evaluation_weight_policy evaluations/fixtures/evaluation_weight_policy_sample.json
    help = "Import evaluation weight policies from a JSON file."

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

        policies = data.get("evaluation_weight_policies")
        if not isinstance(policies, list):
            raise CommandError(
                "JSON must include an 'evaluation_weight_policies' list."
            )

        required_keys = {"uuid", "period_uuid", "position", "category", "weight"}
        totals: dict[tuple[str, str], int] = {}
        for index, policy in enumerate(policies):
            if not isinstance(policy, dict):
                raise CommandError(f"Policy at index {index} must be an object.")
            missing_keys = required_keys - policy.keys()
            if missing_keys:
                missing = ", ".join(sorted(missing_keys))
                raise CommandError(f"Policy at index {index} missing keys: {missing}")

            try:
                period = DbPeriod.objects.get(uuid=policy["period_uuid"])
            except DbPeriod.DoesNotExist as exc:
                raise CommandError(
                    f"Period not found: {policy['period_uuid']}"
                ) from exc

            DbEvaluationWeightPolicy.objects.update_or_create(
                uuid=policy["uuid"],
                defaults={
                    "period": period,
                    "position": policy["position"],
                    "category": policy["category"],
                    "weight": policy["weight"],
                },
            )

            total_key = (policy["period_uuid"], policy["position"])
            totals[total_key] = totals.get(total_key, 0) + int(policy["weight"])

        invalid = [key for key, total in totals.items() if total != 100]
        if invalid:
            formatted = ", ".join([f"{p}:{pos}" for p, pos in invalid])
            raise CommandError(
                f"Weight total must be 100 per period/position. Invalid: {formatted}"
            )

        self.stdout.write(self.style.SUCCESS("Evaluation weight policy import completed."))
