import inject
from rest_framework.exceptions import ValidationError

from evaluations.domain.employee.repository import EmployeeRepository
from evaluations.domain.evaluation_assignment.repository import (
    EvaluationAssignmentRepository,
)
from evaluations.domain.evaluation_item_position_relation.repository import (
    EvaluationItemPositionRelationRepository,
)
from evaluations.domain.evaluation_sheet.entity import EvaluationSheet
from evaluations.domain.evaluation_sheet.repository import EvaluationSheetRepository
from evaluations.domain.evaluation_sheet.score_calculator import (
    calculate_weighted_score,
)
from evaluations.domain.user.entity import User
from evaluations.usecase.evaluation_sheet.dto import (
    EvaluationSheetCreateDto,
    EvaluationSheetEmployeeIdDto,
    EvaluationSheetIdDto,
    EvaluationSheetUpdateDto,
)
from evaluations.usecase.evaluation_sheet.query_service import (
    CategoryScoreSummaryModel,
    EvaluationSheetQueryService,
    EvaluationSheetRawModel,
    EvaluationSheetRetrieveModel,
)
from evaluations.usecase.evaluation_weight_policy.query_service import (
    EvaluationWeightPolicyQueryService,
)


class EvaluationSheetUsecase:
    @inject.autoparams()
    def __init__(
        self,
        evaluation_sheet_repository: EvaluationSheetRepository,
        evaluation_sheet_query_service: EvaluationSheetQueryService,
        evaluation_weight_policy_query_service: EvaluationWeightPolicyQueryService,
        employee_repository: EmployeeRepository,
        evaluation_item_position_relation_repository: EvaluationItemPositionRelationRepository,
        evaluation_assignment_repository: EvaluationAssignmentRepository,
    ):
        self.evaluation_sheet_repository = evaluation_sheet_repository
        self.evaluation_sheet_query_service = evaluation_sheet_query_service
        self.evaluation_weight_policy_query_service = (
            evaluation_weight_policy_query_service
        )
        self.employee_repository = employee_repository
        self.evaluation_item_position_relation_repository = (
            evaluation_item_position_relation_repository
        )
        self.evaluation_assignment_repository = evaluation_assignment_repository

    def _with_weighted_scores(
        self, request_user: User, sheet: EvaluationSheetRawModel
    ) -> EvaluationSheetRetrieveModel:
        employee = self.employee_repository.find_by_id(id=sheet.employee_uuid)
        if not employee:
            return sheet

        weight_policy = self.evaluation_weight_policy_query_service.get_weights(
            request_user, sheet.period_uuid, employee.position
        )
        weight_map = {w.category: w.weight for w in weight_policy.weights}

        own_weighted = calculate_weighted_score(
            [(score.category, score.score) for score in sheet.self_evaluation_score],
            weight_map,
        )
        manager_weighted = calculate_weighted_score(
            [(score.category, score.score) for score in sheet.manager_evaluation_score],
            weight_map,
        )

        own_category_scores = [
            CategoryScoreSummaryModel(
                category=summary.category,
                total=summary.total,
                max_total=summary.max_total,
                weighted_total=summary.weighted_score,
                weighted_max=summary.weight,
            )
            for summary in own_weighted.category_summaries
        ]
        manager_category_scores = [
            CategoryScoreSummaryModel(
                category=summary.category,
                total=summary.total,
                max_total=summary.max_total,
                weighted_total=summary.weighted_score,
                weighted_max=summary.weight,
            )
            for summary in manager_weighted.category_summaries
        ]

        return EvaluationSheetRetrieveModel(
            uuid=sheet.uuid,
            period_uuid=sheet.period_uuid,
            period_name=sheet.period_name,
            employee_uuid=sheet.employee_uuid,
            employee_code=sheet.employee_code,
            employee_name=sheet.employee_name,
            self_evaluation_score=sheet.self_evaluation_score,
            manager_evaluation_score=sheet.manager_evaluation_score,
            own_status=sheet.own_status,
            manager_status=sheet.manager_status,
            own_weighted_total=own_weighted.weighted_total,
            own_weighted_max=own_weighted.weighted_max,
            manager_weighted_total=manager_weighted.weighted_total,
            manager_weighted_max=manager_weighted.weighted_max,
            own_category_scores=own_category_scores,
            manager_category_scores=manager_category_scores,
            created_at=sheet.created_at,
            updated_at=sheet.updated_at,
        )

    def retrieve(
        self, request_user: User, dto: EvaluationSheetIdDto
    ) -> EvaluationSheetRetrieveModel:
        evaluation_sheet = self.evaluation_sheet_query_service.find_by_id(
            request_user, dto.uuid
        )
        if evaluation_sheet is None:
            raise ValidationError("評価シートが見つかりません。")
        evaluation_sheet = self._with_weighted_scores(request_user, evaluation_sheet)
        return evaluation_sheet

    def list_by_employee_id(
        self, request_user: User, dto: EvaluationSheetEmployeeIdDto
    ) -> list[EvaluationSheetRetrieveModel]:
        evaluation_sheets = self.evaluation_sheet_query_service.get_list_by_employee_id(
            request_user, dto.employee_id
        )
        evaluation_sheets = [
            self._with_weighted_scores(request_user, sheet)
            for sheet in evaluation_sheets
        ]
        return evaluation_sheets

    def create(
        self, request_user: User, dto: EvaluationSheetCreateDto
    ) -> EvaluationSheet:
        evaluation_sheet = self.evaluation_sheet_repository.get_by_employee_period(
            request_user, employee_id=dto.employee_id, period_id=dto.period_id
        )
        if evaluation_sheet:
            raise ValidationError("すでに評価シートは存在しています。")

        employee = self.employee_repository.find_by_id(id=dto.employee_id)
        if not employee:
            raise ValidationError("評価対象の従業員が存在しません。")

        evaluation_item_ids = set(
            self.evaluation_item_position_relation_repository.find_item_ids_by_position(
                employee.position
            )
        )

        evaluation_sheet = EvaluationSheet.initialize(
            period_uuid=dto.period_id,
            employee_uuid=dto.employee_id,
            evaluation_item_ids=list(evaluation_item_ids),
        )
        evaluation_sheet = self.evaluation_sheet_repository.create(evaluation_sheet)
        return evaluation_sheet

    def update_own(
        self, request_user: User, dto: EvaluationSheetUpdateDto
    ) -> EvaluationSheet:
        evaluation_sheet = self.evaluation_sheet_repository.find_by_id(
            request_user, id=dto.uuid
        )
        if not evaluation_sheet:
            raise ValidationError("評価シートが存在しません。")
        evaluation_sheet.check_update_own(request_user.employee_uuid)

        employee = self.employee_repository.find_by_id(
            id=evaluation_sheet.employee_uuid
        )
        if not employee:
            raise ValidationError("評価対象の従業員が存在しません。")

        score_dict = {
            sheet_score.evaluation_item_id: sheet_score.score
            for sheet_score in dto.sheet_scores
        }
        if dto.is_temporary:
            evaluation_sheet = evaluation_sheet.save_temporary_own_score(score_dict)
        else:
            evaluation_sheet = evaluation_sheet.complete_own_score(score_dict)

        evaluation_sheet = self.evaluation_sheet_repository.update(evaluation_sheet)
        return evaluation_sheet

    def update_by_manager(
        self, request_user: User, dto: EvaluationSheetUpdateDto
    ) -> EvaluationSheet:
        evaluation_sheet = self.evaluation_sheet_repository.find_by_id(
            request_user, id=dto.uuid
        )
        if not evaluation_sheet:
            raise ValidationError("評価シートが存在しません。")

        employee = self.employee_repository.find_by_id(
            id=evaluation_sheet.employee_uuid
        )
        if not employee:
            raise ValidationError("評価対象の従業員が存在しません。")

        evaluation_assignment = (
            self.evaluation_assignment_repository.find_by_target_employee_id(
                evaluation_sheet.employee_uuid
            )
        )
        if not evaluation_assignment:
            raise ValidationError("この従業員は評価者が割り当てられていません。")
        if evaluation_assignment.manager_employee_uuid != request_user.employee_uuid:
            raise ValidationError("この従業員の評価者ではありません。")

        score_dict = {
            sheet_score.evaluation_item_id: sheet_score.score
            for sheet_score in dto.sheet_scores
        }
        if dto.is_temporary:
            evaluation_sheet = evaluation_sheet.save_temporary_manager_score(score_dict)
        else:
            evaluation_sheet = evaluation_sheet.update_manager_score(score_dict)

        evaluation_sheet = self.evaluation_sheet_repository.update(evaluation_sheet)
        return evaluation_sheet
