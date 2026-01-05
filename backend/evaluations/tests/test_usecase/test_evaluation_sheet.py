from unittest.mock import MagicMock
from uuid import uuid4

from evaluations.usecase.evaluation_sheet.dto import (
    EvaluationSheetCreateDto,
    EvaluationSheetEmployeeIdDto,
    EvaluationSheetIdDto,
    EvaluationSheetScoreDto,
    EvaluationSheetUpdateDto,
)
from evaluations.usecase.evaluation_sheet.usecase import EvaluationSheetUsecase
from evaluations.tests.utils.entity_factory import (
    EmployeeFactory,
    EvaluationSheetFactory,
    EvaluationAssignmentFactory,
    EvaluationSheetScoreFactory,
)
from evaluations.tests.utils.testcase import MyAPITestCase
from rest_framework.exceptions import ValidationError
from evaluations.domain.evaluation_sheet.entity import EvaluationSheetStatusEnum


class EvaluationSheetUsecaseTest(MyAPITestCase):
    def test_retrieve(self) -> None:
        with self.subTest("評価シートが見つからないエラーになること"):
            usecase = EvaluationSheetUsecase()
            usecase.evaluation_sheet_query_service.find_by_id = MagicMock(
                return_value=None
            )
            dto = EvaluationSheetIdDto(uuid4())

            with self.assertRaises(ValidationError) as e:
                usecase.retrieve(dto)

            self.assertEqual(e.exception.detail, ["評価シートが見つかりません。"])

        with self.subTest("正常に取得できること"):
            usecase = EvaluationSheetUsecase()
            entity = EvaluationSheetFactory()
            usecase.evaluation_sheet_query_service.find_by_id = MagicMock(
                return_value=entity
            )
            dto = EvaluationSheetIdDto(uuid4())

            result = usecase.retrieve(dto)

            self.assertIsNotNone(result)

    def test_list_by_employee_id(self) -> None:
        with self.subTest("従業員IDで一覧取得できること"):
            usecase = EvaluationSheetUsecase()
            expected = [EvaluationSheetFactory(), EvaluationSheetFactory()]
            usecase.evaluation_sheet_query_service.get_list_by_employee_id = MagicMock(
                return_value=expected
            )
            dto = EvaluationSheetEmployeeIdDto(uuid4())

            result = usecase.list_by_employee_id(dto)

            self.assertEqual(result, expected)

    def test_create(self) -> None:
        with self.subTest("すでに評価シートが存在する場合にエラーになること"):
            usecase = EvaluationSheetUsecase()
            usecase.evaluation_sheet_repository.get_by_employee_period = MagicMock(
                return_value=EvaluationSheetFactory()
            )
            dto = EvaluationSheetCreateDto(uuid4(), uuid4())

            with self.assertRaises(ValidationError) as e:
                usecase.create(dto)

            self.assertEqual(e.exception.detail, ["すでに評価シートは存在しています。"])

        with self.subTest("正常に作成できること"):
            usecase = EvaluationSheetUsecase()
            employee_id = uuid4()
            period_id = uuid4()
            usecase.evaluation_sheet_repository.get_by_employee_period = MagicMock(
                return_value=None
            )
            employee = EmployeeFactory(uuid=employee_id)
            usecase.employee_repository.find_by_id = MagicMock(return_value=employee)
            item_id1 = uuid4()
            item_id2 = uuid4()
            usecase.evaluation_item_position_relation_repository.find_item_ids_by_position = MagicMock(
                return_value=[item_id1, item_id2]
            )
            created_sheet = EvaluationSheetFactory(
                employee_uuid=employee_id, period_uuid=period_id
            )
            usecase.evaluation_sheet_repository.create = MagicMock(
                return_value=created_sheet
            )
            dto = EvaluationSheetCreateDto(employee_id, period_id)

            result = usecase.create(dto)

            self.assertEqual(result, created_sheet)

    def test_update_own(self) -> None:
        with self.subTest("評価シートが存在しない場合にエラーになること"):
            usecase = EvaluationSheetUsecase()
            usecase.evaluation_sheet_repository.find_by_id = MagicMock(
                return_value=None
            )
            dto = EvaluationSheetUpdateDto(uuid4(), uuid4(), [], True)

            with self.assertRaises(ValidationError) as e:
                usecase.update_own(dto)

            self.assertEqual(e.exception.detail, ["評価シートが存在しません。"])

        with self.subTest("更新者が一致しない場合にエラーになること"):
            usecase = EvaluationSheetUsecase()
            entity = EvaluationSheetFactory(employee_uuid=uuid4())
            usecase.evaluation_sheet_repository.find_by_id = MagicMock(
                return_value=entity
            )
            dto = EvaluationSheetUpdateDto(uuid4(), uuid4(), [], True)

            with self.assertRaises(ValidationError) as e:
                usecase.update_own(dto)

            self.assertEqual(
                e.exception.detail, ["更新者と評価シートの対象者が一致していません。"]
            )

        with self.subTest("評価対象の従業員が存在しない場合にエラーになること"):
            usecase = EvaluationSheetUsecase()
            employee_id = uuid4()
            entity = EvaluationSheetFactory(employee_uuid=employee_id)
            usecase.evaluation_sheet_repository.find_by_id = MagicMock(
                return_value=entity
            )
            usecase.employee_repository.find_by_id = MagicMock(return_value=None)
            dto = EvaluationSheetUpdateDto(uuid4(), employee_id, [], True)

            with self.assertRaises(ValidationError) as e:
                usecase.update_own(dto)

            self.assertEqual(e.exception.detail, ["評価対象の従業員が存在しません。"])

        with self.subTest("正常に更新できること"):
            usecase = EvaluationSheetUsecase()
            employee_id = uuid4()
            item_id1 = uuid4()
            item_id2 = uuid4()
            own_scores = [
                EvaluationSheetScoreFactory(evaluation_item_uuid=item_id1),
                EvaluationSheetScoreFactory(evaluation_item_uuid=item_id2),
            ]
            entity = EvaluationSheetFactory(
                employee_uuid=employee_id, own_scores=own_scores
            )
            usecase.evaluation_sheet_repository.find_by_id = MagicMock(
                return_value=entity
            )
            employee = EmployeeFactory(uuid=employee_id)
            usecase.employee_repository.find_by_id = MagicMock(return_value=employee)
            usecase.evaluation_sheet_repository.update = MagicMock(return_value=entity)
            dto = EvaluationSheetUpdateDto(
                uuid4(),
                employee_id,
                [
                    EvaluationSheetScoreDto(item_id1, 3),
                    EvaluationSheetScoreDto(item_id2, 4),
                ],
                False,
            )

            result = usecase.update_own(dto)

            self.assertIsNotNone(result)
            self.assertEqual(result.uuid, entity.uuid)
            self.assertEqual(result.employee_uuid, employee_id)
            self.assertEqual(result.status, EvaluationSheetStatusEnum.SELF_COMPLETED)
            self.assertEqual(result.own_scores[0].score, 3)
            self.assertEqual(result.own_scores[1].score, 4)

    def test_update_by_manager(self) -> None:
        with self.subTest("評価シートが存在しない場合にエラーになること"):
            usecase = EvaluationSheetUsecase()
            usecase.evaluation_sheet_repository.find_by_id = MagicMock(
                return_value=None
            )
            dto = EvaluationSheetUpdateDto(uuid4(), uuid4(), [], True)

            with self.assertRaises(ValidationError) as e:
                usecase.update_by_manager(dto)

            self.assertEqual(e.exception.detail, ["評価シートが存在しません。"])

        with self.subTest("評価対象の従業員が存在しない場合にエラーになること"):
            usecase = EvaluationSheetUsecase()
            employee_id = uuid4()
            entity = EvaluationSheetFactory(employee_uuid=employee_id)
            usecase.evaluation_sheet_repository.find_by_id = MagicMock(
                return_value=entity
            )
            usecase.employee_repository.find_by_id = MagicMock(return_value=None)
            dto = EvaluationSheetUpdateDto(uuid4(), uuid4(), [], True)

            with self.assertRaises(ValidationError) as e:
                usecase.update_by_manager(dto)

            self.assertEqual(e.exception.detail, ["評価対象の従業員が存在しません。"])

        with self.subTest("評価者が割り当てられていない場合にエラーになること"):
            usecase = EvaluationSheetUsecase()
            usecase.evaluation_assignment_repository = MagicMock()
            employee_id = uuid4()
            entity = EvaluationSheetFactory(employee_uuid=employee_id)
            usecase.evaluation_sheet_repository.find_by_id = MagicMock(
                return_value=entity
            )
            employee = EmployeeFactory(uuid=employee_id)
            usecase.employee_repository.find_by_id = MagicMock(return_value=employee)
            usecase.evaluation_assignment_repository.find_by_target_employee_id = (
                MagicMock(return_value=None)
            )
            dto = EvaluationSheetUpdateDto(uuid4(), uuid4(), [], True)

            with self.assertRaises(ValidationError) as e:
                usecase.update_by_manager(dto)

            self.assertEqual(
                e.exception.detail, ["この従業員は評価者が割り当てられていません。"]
            )

        with self.subTest("評価者ではない場合にエラーになること"):
            usecase = EvaluationSheetUsecase()
            employee_id = uuid4()
            entity = EvaluationSheetFactory(employee_uuid=employee_id)
            usecase.evaluation_sheet_repository.find_by_id = MagicMock(
                return_value=entity
            )
            employee = EmployeeFactory(uuid=employee_id)
            usecase.employee_repository.find_by_id = MagicMock(return_value=employee)
            assignment = EvaluationAssignmentFactory(target_employee_uuid=employee_id)
            usecase.evaluation_assignment_repository.find_by_target_employee_id = (
                MagicMock(return_value=assignment)
            )
            dto = EvaluationSheetUpdateDto(uuid4(), uuid4(), [], True)

            with self.assertRaises(ValidationError) as e:
                usecase.update_by_manager(dto)

            self.assertEqual(e.exception.detail, ["この従業員の評価者ではありません。"])

        with self.subTest("正常に更新できること"):
            usecase = EvaluationSheetUsecase()
            usecase.evaluation_sheet_repository = MagicMock()
            usecase.employee_repository = MagicMock()
            usecase.evaluation_assignment_repository = MagicMock()
            employee_id = uuid4()
            manager_id = uuid4()
            item_id1 = uuid4()
            item_id2 = uuid4()
            manager_scores = [
                EvaluationSheetScoreFactory(evaluation_item_uuid=item_id1),
                EvaluationSheetScoreFactory(evaluation_item_uuid=item_id2),
            ]
            entity = EvaluationSheetFactory(
                employee_uuid=employee_id, manager_scores=manager_scores
            )
            usecase.evaluation_sheet_repository.find_by_id = MagicMock(
                return_value=entity
            )
            employee = EmployeeFactory(uuid=employee_id)
            usecase.employee_repository.find_by_id = MagicMock(return_value=employee)
            assignment = EvaluationAssignmentFactory(
                target_employee_uuid=employee_id,
                manager_employee_uuid=manager_id,
            )
            usecase.evaluation_assignment_repository.find_by_target_employee_id = (
                MagicMock(return_value=assignment)
            )
            usecase.evaluation_sheet_repository.update = MagicMock(return_value=entity)
            dto = EvaluationSheetUpdateDto(
                uuid4(),
                manager_id,
                [
                    EvaluationSheetScoreDto(item_id1, 3),
                    EvaluationSheetScoreDto(item_id2, 4),
                ],
                False,
            )

            result = usecase.update_by_manager(dto)

            self.assertIsNotNone(result)
            self.assertEqual(result.uuid, entity.uuid)
            self.assertEqual(result.employee_uuid, employee_id)
            self.assertEqual(result.status, EvaluationSheetStatusEnum.MANAGER_COMPLETED)
            self.assertEqual(result.manager_scores[0].score, 3)
            self.assertEqual(result.manager_scores[1].score, 4)
