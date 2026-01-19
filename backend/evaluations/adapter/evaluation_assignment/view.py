from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from evaluations.usecase.evaluation_assignment.usecase import (
    EvaluationAssignmentUsecase,
)
from evaluations.utils.dataclass import asdict
from evaluations.utils.user import to_user_entity


class EvaluationAssignmentViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request: Request) -> Response:
        usecase = EvaluationAssignmentUsecase()
        targets = usecase.get_list_manager_targets(to_user_entity(request.user))
        return Response([asdict(target) for target in targets])
