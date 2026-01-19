from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from evaluations.usecase.period.usecase import PeriodUsecase
from evaluations.utils.dataclass import asdict
from evaluations.utils.user import to_user_entity


class PeriodViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request: Request) -> Response:
        usecase = PeriodUsecase()
        period_list = usecase.get_periods(to_user_entity(request.user))
        return Response(asdict(period_list))
