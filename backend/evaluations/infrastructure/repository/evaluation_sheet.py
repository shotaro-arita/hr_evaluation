from uuid import UUID

from django.db import transaction
from rest_framework.exceptions import ValidationError

from evaluations.domain.evaluation_sheet.entity import (
    EvaluationSheet,
    EvaluationSheetScore,
)
from evaluations.domain.evaluation_sheet.repository import EvaluationSheetRepository
from evaluations.models.evaluation_sheet import (
    DbEvaluationSheet,
    DbEvaluationSheetScore,
)


class EvaluationSheetRepositoryImpl(EvaluationSheetRepository):
    def find_by_id(self, id: UUID) -> EvaluationSheet | None:
        try:
            sheet = DbEvaluationSheet.objects.prefetch_related("scores").get(uuid=id)
        except DbEvaluationSheet.DoesNotExist:
            return None
        return sheet.to_entity()

    def get_by_employee_period(
        self, employee_id: UUID, period_id: UUID
    ) -> EvaluationSheet | None:
        try:
            sheet = DbEvaluationSheet.objects.prefetch_related("scores").get(
                employee_id=employee_id, period_id=period_id
            )
        except DbEvaluationSheet.DoesNotExist:
            return None
        return sheet.to_entity()

    def _set_sheet_model(
        self,
        evaluation_sheet_model: DbEvaluationSheet,
        evaluation_sheet: EvaluationSheet,
    ) -> EvaluationSheet:
        evaluation_sheet_model.period_id = evaluation_sheet.period_uuid
        evaluation_sheet_model.employee_id = evaluation_sheet.employee_uuid
        evaluation_sheet_model.status = evaluation_sheet.status.value
        return evaluation_sheet_model

    def _create_scores(
        self,
        evaluation_sheet_model: DbEvaluationSheet,
        evaluation_sheet: EvaluationSheet,
    ) -> None:
        score_models: list[DbEvaluationSheetScore] = []
        for score in evaluation_sheet.own_scores:
            score_models.append(
                self._set_score_model(evaluation_sheet_model, None, score, False)
            )
        for score in evaluation_sheet.manager_scores:
            score_models.append(
                self._set_score_model(evaluation_sheet_model, None, score, True)
            )
        DbEvaluationSheetScore.objects.bulk_create(score_models)

    def _set_score_model(
        self,
        evaluation_sheet_model: DbEvaluationSheet,
        score_model: DbEvaluationSheetScore | None,
        score: EvaluationSheetScore,
        is_manager: bool,
    ) -> DbEvaluationSheetScore:
        if score_model is None:
            score_model = DbEvaluationSheetScore(
                uuid=score.uuid,
                evaluation_sheet=evaluation_sheet_model,
            )
        score_model.evaluation_item_id = score.evaluation_item_uuid
        score_model.score = score.score
        score_model.is_manager = is_manager
        return score_model

    @transaction.atomic
    def create(self, evaluation_sheet: EvaluationSheet) -> EvaluationSheet:
        evaluation_sheet_model = DbEvaluationSheet(uuid=evaluation_sheet.uuid)
        evaluation_sheet_model = self._set_sheet_model(
            evaluation_sheet_model, evaluation_sheet
        )
        evaluation_sheet_model.save()

        self._create_scores(evaluation_sheet_model, evaluation_sheet)
        evaluation_sheet_model.refresh_from_db()
        return evaluation_sheet_model.to_entity()

    @transaction.atomic
    def update(self, evaluation_sheet: EvaluationSheet) -> EvaluationSheet:
        try:
            evaluation_sheet_model = DbEvaluationSheet.objects.get(
                uuid=evaluation_sheet.uuid
            )
        except DbEvaluationSheet.DoesNotExist as e:
            raise ValidationError("評価シートが見つかりません") from e

        evaluation_sheet_model = self._set_sheet_model(
            evaluation_sheet_model, evaluation_sheet
        )
        evaluation_sheet_model.save()

        self._sync_scores(evaluation_sheet_model, evaluation_sheet)
        evaluation_sheet_model.refresh_from_db()
        return evaluation_sheet_model.to_entity()

    def _sync_scores(
        self,
        evaluation_sheet_model: DbEvaluationSheet,
        evaluation_sheet: EvaluationSheet,
    ) -> None:
        desired_scores: list[tuple] = []
        for score in evaluation_sheet.own_scores:
            desired_scores.append((score, False))
        for score in evaluation_sheet.manager_scores:
            desired_scores.append((score, True))

        desired_ids = {score.uuid for score, _ in desired_scores}
        existing = DbEvaluationSheetScore.objects.filter(
            evaluation_sheet=evaluation_sheet_model
        ).in_bulk(field_name="uuid")

        to_create: list[DbEvaluationSheetScore] = []
        to_update: list[DbEvaluationSheetScore] = []
        for score, is_manager in desired_scores:
            existing_model = existing.get(score.uuid)
            if existing_model is None:
                to_create.append(
                    self._set_score_model(
                        evaluation_sheet_model, None, score, is_manager
                    )
                )
                continue
            self._set_score_model(
                evaluation_sheet_model, existing_model, score, is_manager
            )
            to_update.append(existing_model)

        delete_ids = [uuid for uuid in existing.keys() if uuid not in desired_ids]
        if delete_ids:
            DbEvaluationSheetScore.objects.filter(uuid__in=delete_ids).delete()
        if to_create:
            DbEvaluationSheetScore.objects.bulk_create(to_create)
        if to_update:
            DbEvaluationSheetScore.objects.bulk_update(
                to_update, ["evaluation_item_id", "score", "is_manager"]
            )
