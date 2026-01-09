from unittest.mock import patch

from rest_framework import status

from evaluations.tests.utils.entity_factory import EvaluationSheetFactory, UserFactory
from evaluations.usecase.evaluation_sheet.usecase import EvaluationSheetUsecase
from evaluations.tests.utils.testcase import MyAPITestCase
from evaluations.usecase.evaluation_sheet.dto import (
    EvaluationSheetCreateDto,
    EvaluationSheetEmployeeIdDto,
    EvaluationSheetIdDto,
    EvaluationSheetScoreDto,
    EvaluationSheetUpdateDto,
)
from uuid import uuid4
from evaluations.tests.utils.model_factory import DbUserFactory


class SubmissionGroupHospitalViewSetTests(MyAPITestCase):
    url = "/api/evaluations/evaluation_sheets"

    def test_retrieve(self) -> None:
        with patch.object(EvaluationSheetUsecase, "retrieve") as mock:
            evaluation_sheet = EvaluationSheetFactory()
            mock.return_value = evaluation_sheet
            user = DbUserFactory()
            self.client.force_authenticate(user=user)
            user_entity = user.to_entity

            response = self.client.get(f"{self.url}/{evaluation_sheet.uuid}/")

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(
                mock.call_args[0][0],
                user_entity,
            )
            self.assertEqual(
                mock.call_args[0][1], EvaluationSheetIdDto(uuid=evaluation_sheet.uuid)
            )

    def test_list(self) -> None:
        with patch.object(EvaluationSheetUsecase, "list_by_employee_id") as mock:
            employee_id = uuid4()
            mock.return_value = [EvaluationSheetFactory(), EvaluationSheetFactory()]
            user = DbUserFactory()
            self.client.force_authenticate(user=user)

            response = self.client.get(f"{self.url}/?employee_id={employee_id}")

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(
                mock.call_args[0][1],
                EvaluationSheetEmployeeIdDto(employee_id=employee_id),
            )

    def test_create(self) -> None:
        with patch.object(EvaluationSheetUsecase, "create") as mock:
            employee_id = uuid4()
            period_id = uuid4()
            mock.return_value = EvaluationSheetFactory(
                employee_uuid=employee_id, period_uuid=period_id
            )
            user = DbUserFactory()
            self.client.force_authenticate(user=user)

            response = self.client.post(
                f"{self.url}/",
                {"employee_id": str(employee_id), "period_id": str(period_id)},
                format="json",
            )

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(
                mock.call_args[0][1],
                EvaluationSheetCreateDto(employee_id=employee_id, period_id=period_id),
            )

    def test_update_own(self) -> None:
        with patch.object(EvaluationSheetUsecase, "update_own") as mock:
            sheet_id = uuid4()
            item_id = uuid4()
            mock.return_value = EvaluationSheetFactory(uuid=sheet_id)
            user = DbUserFactory()
            self.client.force_authenticate(user=user)

            response = self.client.put(
                f"{self.url}/{sheet_id}/update_own/",
                {
                    "sheet_scores": [{"evaluation_item_id": str(item_id), "score": 3}],
                    "is_temporary": False,
                },
                format="json",
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(
                mock.call_args[0][1],
                EvaluationSheetUpdateDto(
                    uuid=sheet_id,
                    sheet_scores=[EvaluationSheetScoreDto(item_id, 3)],
                    is_temporary=False,
                ),
            )

    def test_update_by_manager(self) -> None:
        with patch.object(EvaluationSheetUsecase, "update_by_manager") as mock:
            sheet_id = uuid4()
            item_id = uuid4()
            mock.return_value = EvaluationSheetFactory(uuid=sheet_id)
            user = DbUserFactory()
            self.client.force_authenticate(user=user)

            response = self.client.put(
                f"{self.url}/{sheet_id}/update_by_manager/",
                {
                    "sheet_scores": [{"evaluation_item_id": str(item_id), "score": 4}],
                    "is_temporary": True,
                },
                format="json",
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(
                mock.call_args[0][1],
                EvaluationSheetUpdateDto(
                    uuid=sheet_id,
                    sheet_scores=[EvaluationSheetScoreDto(item_id, 4)],
                    is_temporary=True,
                ),
            )
