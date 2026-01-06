from uuid import UUID

from evaluations.models.employee import DbEmployee
from evaluations.domain.employee.repository import EmployeeRepository
from evaluations.domain.employee.entity import Employee


class EmployeeRepositoryImpl(EmployeeRepository):
    def find_by_id(self, id: UUID) -> Employee | None:
        try:
            employee_model = DbEmployee.objects.get(uuid=id)
        except DbEmployee.DoesNotExist:
            return None
        return employee_model.to_entity()
