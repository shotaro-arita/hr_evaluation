from uuid import UUID

from evaluations.domain.evaluation_item.entity import EvaluationItemCategory
from evaluations.domain.evaluation_sheet.entity import EvaluationSheetStatusEnum
from evaluations.models.employee import DbEmployee
from evaluations.models.evaluation_item import DbEvaluationItem
from evaluations.models.evaluation_sheet import DbEvaluationSheet
from evaluations.models.period import DbPeriod
from evaluations.usecase.evaluation_sheet.query_service import (
    EvaluationScoreRetrieveModel,
    EvaluationSheetQueryService,
    EvaluationSheetRetrieveModel,
)


class EvaluationSheetQueryServiceImpl(EvaluationSheetQueryService):
    def find_by_id(self, id: UUID) -> EvaluationSheetRetrieveModel | None:
        try:
            sheet_model = DbEvaluationSheet.objects.prefetch_related("scores").get(
                uuid=id
            )
        except DbEvaluationSheet.DoesNotExist:
            return None
        return self._to_retrieve_model(sheet_model)

    def get_list_by_employee_id(
        self, employee_id: UUID
    ) -> list[EvaluationSheetRetrieveModel]:
        sheet_models = DbEvaluationSheet.objects.prefetch_related("scores").filter(
            employee_uuid=employee_id
        )
        return [self._to_retrieve_model(sheet_model) for sheet_model in sheet_models]

    def _to_retrieve_model(
        self, sheet_model: DbEvaluationSheet
    ) -> EvaluationSheetRetrieveModel:
        score_models = list(sheet_model.scores.all())
        item_ids = [score.evaluation_item_uuid for score in score_models]
        item_model_map = {
            item.uuid: item
            for item in DbEvaluationItem.objects.filter(uuid__in=item_ids)
        }
        self_scores: list[EvaluationScoreRetrieveModel] = []
        manager_scores: list[EvaluationScoreRetrieveModel] = []
        for score_model in score_models:
            item_model = item_model_map.get(score_model.evaluation_item_uuid)
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

        period = DbPeriod.objects.filter(uuid=sheet_model.period_uuid).first()
        employee = DbEmployee.objects.filter(uuid=sheet_model.employee_uuid).first()
        return EvaluationSheetRetrieveModel(
            uuid=sheet_model.uuid,
            period_uuid=sheet_model.period_uuid,
            period_name=period.name if period else "",
            employee_uuid=sheet_model.employee_uuid,
            employee_code=employee.employee_code if employee else "",
            employee_name=employee.name if employee else "",
            self_evaluation_score=self_scores,
            manager_evaluation_score=manager_scores,
            status=EvaluationSheetStatusEnum(sheet_model.status),
            created_at=sheet_model.created_at,
            updated_at=sheet_model.updated_at,
        )
