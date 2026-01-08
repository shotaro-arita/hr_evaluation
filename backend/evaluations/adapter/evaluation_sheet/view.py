from typing import Any
from uuid import UUID

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from evaluations.adapter.evaluation_sheet.serializer import (
    EvaluationSheetCreateDtoSerializer,
    EvaluationSheetEmployeeIdDtoSerializer,
    EvaluationSheetIdDtoSerializer,
    EvaluationSheetUpdateDtoSerializer,
)
from evaluations.usecase.evaluation_sheet.usecase import EvaluationSheetUsecase
from evaluations.utils.dataclass import asdict
from evaluations.utils.user import to_user_entity


class EvaluationSheetViewSet(viewsets.ViewSet):
    lookup_field = "uuid"
    permission_classes = [IsAuthenticated]

    def retrieve(self, request: Request, uuid: UUID) -> Response:
        serializer = EvaluationSheetIdDtoSerializer(data={"uuid": uuid})
        serializer.is_valid(raise_exception=True)
        usecase = EvaluationSheetUsecase()
        evaluation_sheet = usecase.retrieve(
            to_user_entity(request.user), serializer.validated_data
        )
        return Response(asdict(evaluation_sheet))

    def list(self, request: Request) -> Response:
        serializer = EvaluationSheetEmployeeIdDtoSerializer(
            data={"employee_id": request.query_params.get("employee_id")}
        )
        serializer.is_valid(raise_exception=True)
        usecase = EvaluationSheetUsecase()
        evaluation_sheets = usecase.list_by_employee_id(
            to_user_entity(request.user), serializer.validated_data
        )
        return Response([asdict(sheet) for sheet in evaluation_sheets])

    def create(self, request: Request) -> Response:
        serializer = EvaluationSheetCreateDtoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        usecase = EvaluationSheetUsecase()
        evaluation_sheet = usecase.create(
            to_user_entity(request.user), serializer.validated_data
        )
        return Response(asdict(evaluation_sheet), status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["PUT"])
    def update_own(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        sheet_uuid = UUID(str(kwargs["uuid"]))
        payload = {**request.data, "uuid": sheet_uuid}
        serializer = EvaluationSheetUpdateDtoSerializer(data=payload)
        serializer.is_valid(raise_exception=True)
        usecase = EvaluationSheetUsecase()
        evaluation_sheet = usecase.update_own(
            to_user_entity(request.user), serializer.validated_data
        )
        return Response(asdict(evaluation_sheet))

    @action(detail=True, methods=["PUT"])
    def update_by_manager(
        self, request: Request, *args: Any, **kwargs: Any
    ) -> Response:
        sheet_uuid = UUID(str(kwargs["uuid"]))
        payload = {**request.data, "uuid": sheet_uuid}
        serializer = EvaluationSheetUpdateDtoSerializer(data=payload)
        serializer.is_valid(raise_exception=True)
        usecase = EvaluationSheetUsecase()
        evaluation_sheet = usecase.update_by_manager(
            to_user_entity(request.user), serializer.validated_data
        )
        return Response(asdict(evaluation_sheet))
