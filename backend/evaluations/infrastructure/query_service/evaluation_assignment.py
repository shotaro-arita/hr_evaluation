from evaluations.domain.user.entity import User
from evaluations.models.evaluation_assignment import DbEvaluationAssignment
from evaluations.usecase.evaluation_assignment.query_service import (
    EvaluationAssignmentQueryService,
    ManagerTargetModel,
)


class EvaluationAssignmentQueryServiceImpl(EvaluationAssignmentQueryService):
    def get_manager_targets(self, user: User) -> list[ManagerTargetModel]:
        assignments = (
            DbEvaluationAssignment.objects.select_related("target_employee")
            .filter(manager_employee_id=user.employee_uuid)
            .order_by("target_employee__employee_code")
        )
        targets = []
        for assignment in assignments:
            target = assignment.target_employee
            targets.append(
                ManagerTargetModel(
                    employee_uuid=target.uuid,
                    employee_code=target.employee_code,
                    name=target.name,
                    position=target.position,
                    job_type=target.job_type,
                    role=assignment.role,
                )
            )
        return targets
