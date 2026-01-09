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
from evaluations.domain.user.entity import User
from evaluations.usecase.evaluation_sheet.dto import (
    EvaluationSheetCreateDto,
    EvaluationSheetEmployeeIdDto,
    EvaluationSheetIdDto,
    EvaluationSheetUpdateDto,
)
from evaluations.usecase.evaluation_sheet.query_service import (
    EvaluationSheetQueryService,
    EvaluationSheetRetrieveModel,
)


class EvaluationSheetUsecase:
    @inject.autoparams()
    def __init__(
        self,
        evaluation_sheet_repository: EvaluationSheetRepository,
        evaluation_sheet_query_service: EvaluationSheetQueryService,
        employee_repository: EmployeeRepository,
        evaluation_item_position_relation_repository: EvaluationItemPositionRelationRepository,
        evaluation_assignment_repository: EvaluationAssignmentRepository,
    ):
        self.evaluation_sheet_repository = evaluation_sheet_repository
        self.evaluation_sheet_query_service = evaluation_sheet_query_service
        self.employee_repository = employee_repository
        self.evaluation_item_position_relation_repository = (
            evaluation_item_position_relation_repository
        )
        self.evaluation_assignment_repository = evaluation_assignment_repository

    def retrieve(
        self, request_user: User, dto: EvaluationSheetIdDto
    ) -> EvaluationSheetRetrieveModel:
        evaluation_sheet = self.evaluation_sheet_query_service.find_by_id(
            request_user, dto.uuid
        )
        if evaluation_sheet is None:
            raise ValidationError("評価シートが見つかりません。")
        return evaluation_sheet

    def list_by_employee_id(
        self, request_user: User, dto: EvaluationSheetEmployeeIdDto
    ) -> list[EvaluationSheetRetrieveModel]:
        evaluation_sheets = self.evaluation_sheet_query_service.get_list_by_employee_id(
            request_user, dto.employee_id
        )
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
            evaluation_item_ids=evaluation_item_ids,
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
            evaluation_sheet = evaluation_sheet.save_temporary_manager_score(score_dict)
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
