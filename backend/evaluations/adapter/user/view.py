from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from evaluations.usecase.user.usecase import UserUsecase
from evaluations.utils.dataclass import asdict
from evaluations.utils.user import to_user_entity


class UserViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request: Request) -> Response:
        usecase = UserUsecase()
        user = usecase.get_user(to_user_entity(request.user))
        return Response(asdict(user))
