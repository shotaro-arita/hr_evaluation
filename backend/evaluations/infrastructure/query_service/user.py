from evaluations.domain.user.entity import User
from evaluations.models.evaluation_assignment import DbEvaluationAssignment
from evaluations.models.user import DbUser
from evaluations.usecase.user.query_service import UserQueryService, UserRetrieveModel


class UserQueryServiceImpl(UserQueryService):
    def get_user(self, user: User) -> UserRetrieveModel | None:
        try:
            user_model = DbUser.objects.select_related("employee").get(uuid=user.uuid)
        except DbUser.DoesNotExist:
            return None

        employee = user_model.employee
        manager_target_count = DbEvaluationAssignment.objects.filter(
            manager_employee_id=employee.uuid
        ).count()

        return UserRetrieveModel(
            user_uuid=user_model.uuid,
            employee_uuid=employee.uuid,
            employee_code=employee.employee_code,
            name=user_model.name,
            position=employee.position,
            job_type=employee.job_type,
            is_manager=manager_target_count > 0,
            manager_target_count=manager_target_count,
        )
