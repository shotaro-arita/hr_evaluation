from uuid import UUID

from evaluations.domain.evaluation_item.entity import EvaluationItemCategory
from evaluations.domain.evaluation_sheet.entity import EvaluationSheetStatusEnum
from evaluations.models.evaluation_assignment import DbEvaluationAssignment
from evaluations.models.evaluation_sheet import DbEvaluationSheet
from evaluations.usecase.evaluation_sheet.query_service import (
    EvaluationScoreRetrieveModel,
    EvaluationSheetQueryService,
    EvaluationSheetRawModel,
)
from evaluations.domain.user.entity import User


class EvaluationSheetQueryServiceImpl(EvaluationSheetQueryService):
    def _get_allowed_employee_ids(self, user: User) -> set[UUID]:
        manager_targets = DbEvaluationAssignment.objects.filter(
            manager_employee_id=user.employee_uuid
        ).values_list("target_employee_id", flat=True)
        return {user.employee_uuid, *set(manager_targets)}

    def find_by_id(self, user: User, id: UUID) -> EvaluationSheetRawModel | None:
        allowed_employee_ids = self._get_allowed_employee_ids(user)
        try:
            sheet_model = (
                DbEvaluationSheet.objects.select_related("period", "employee")
                .prefetch_related("scores__evaluation_item")
                .get(uuid=id, employee_id__in=allowed_employee_ids)
            )
        except DbEvaluationSheet.DoesNotExist:
            return None
        return self._to_retrieve_model(sheet_model)

    def get_list_by_employee_id(
        self, user: User, employee_id: UUID
    ) -> list[EvaluationSheetRawModel]:
        allowed_employee_ids = self._get_allowed_employee_ids(user)
        if employee_id not in allowed_employee_ids:
            return []
        sheet_models = (
            DbEvaluationSheet.objects.select_related("period", "employee")
            .prefetch_related("scores__evaluation_item")
            .filter(employee_id=employee_id)
        )
        return [self._to_retrieve_model(sheet_model) for sheet_model in sheet_models]

    def _to_retrieve_model(
        self, sheet_model: DbEvaluationSheet
    ) -> EvaluationSheetRawModel:
        score_models = list(sheet_model.scores.all())
        self_scores: list[EvaluationScoreRetrieveModel] = []
        manager_scores: list[EvaluationScoreRetrieveModel] = []
        for score_model in score_models:
            item_model = score_model.evaluation_item
            if item_model is None:
                continue
            model = EvaluationScoreRetrieveModel(
                uuid=score_model.uuid,
                item_uuid=item_model.uuid,
                title=item_model.title,
                category=EvaluationItemCategory(item_model.category),
                description=item_model.description,
                criteria_1=item_model.criteria_1,
                criteria_2=item_model.criteria_2,
                criteria_3=item_model.criteria_3,
                criteria_4=item_model.criteria_4,
                criteria_5=item_model.criteria_5,
                score=score_model.score,
            )
            if score_model.is_manager:
                manager_scores.append(model)
            else:
                self_scores.append(model)

        return EvaluationSheetRawModel(
            uuid=sheet_model.uuid,
            period_uuid=sheet_model.period_id,
            period_name=sheet_model.period.name,
            employee_uuid=sheet_model.employee_id,
            employee_code=sheet_model.employee.employee_code,
            employee_name=sheet_model.employee.name,
            self_evaluation_score=self_scores,
            manager_evaluation_score=manager_scores,
            own_status=EvaluationSheetStatusEnum(sheet_model.own_status),
            manager_status=EvaluationSheetStatusEnum(sheet_model.manager_status),
            created_at=sheet_model.created_at,
            updated_at=sheet_model.updated_at,
        )
