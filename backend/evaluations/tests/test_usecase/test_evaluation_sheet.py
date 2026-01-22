from unittest.mock import MagicMock
from uuid import uuid4

from rest_framework.exceptions import ValidationError

from evaluations.domain.evaluation_item.entity import EvaluationItemCategory
from evaluations.domain.evaluation_sheet.entity import EvaluationSheetStatusEnum
from evaluations.tests.utils.entity_factory import (
    EmployeeFactory,
    EvaluationAssignmentFactory,
    EvaluationScoreRetrieveModelFactory,
    EvaluationSheetFactory,
    EvaluationSheetRawModelFactory,
    EvaluationSheetScoreFactory,
    UserFactory,
)
from evaluations.tests.utils.testcase import MyAPITestCase
from evaluations.usecase.evaluation_sheet.dto import (
    EvaluationSheetCreateDto,
    EvaluationSheetEmployeeIdDto,
    EvaluationSheetIdDto,
    EvaluationSheetScoreDto,
    EvaluationSheetUpdateDto,
)
from evaluations.usecase.evaluation_sheet.usecase import EvaluationSheetUsecase
from evaluations.usecase.evaluation_weight_policy.query_service import (
    EvaluationWeightModel,
    EvaluationWeightPolicyListModel,
)


class EvaluationSheetUsecaseTest(MyAPITestCase):
    def test_retrieve(self) -> None:
        with self.subTest("評価シートが見つからないエラーになること"):
            usecase = EvaluationSheetUsecase()
            usecase.evaluation_sheet_query_service.find_by_id = MagicMock(
                return_value=None
            )
            dto = EvaluationSheetIdDto(uuid4())
            request_user = UserFactory()

            with self.assertRaises(ValidationError) as e:
                usecase.retrieve(request_user, dto)

            self.assertEqual(e.exception.detail, ["評価シートが見つかりません。"])

        with self.subTest("正常に取得できること"):
            usecase = EvaluationSheetUsecase()
            employee_id = uuid4()
            own_score = EvaluationScoreRetrieveModelFactory(
                category=EvaluationItemCategory.PERFORMANCE_RESULTS,
                score=3,
            )
            manager_score = EvaluationScoreRetrieveModelFactory(
                category=EvaluationItemCategory.ATTITUDE_SKILLS,
                score=4,
            )
            entity = EvaluationSheetRawModelFactory(
                employee_uuid=employee_id,
                self_evaluation_score=[own_score],
                manager_evaluation_score=[manager_score],
                own_status=EvaluationSheetStatusEnum.COMPLETED,
                manager_status=EvaluationSheetStatusEnum.DRAFT,
            )
            usecase.evaluation_sheet_query_service.find_by_id = MagicMock(
                return_value=entity
            )
            usecase.employee_repository.find_by_id = MagicMock(
                return_value=EmployeeFactory(uuid=employee_id)
            )
            usecase.evaluation_weight_policy_query_service.get_weights = MagicMock(
                side_effect=lambda _user,
                period_id,
                position: EvaluationWeightPolicyListModel(
                    period_uuid=period_id,
                    position=position,
                    weights=[
                        EvaluationWeightModel(
                            category=EvaluationItemCategory.PERFORMANCE_RESULTS,
                            weight=60,
                        ),
                        EvaluationWeightModel(
                            category=EvaluationItemCategory.ATTITUDE_SKILLS, weight=40
                        ),
                    ],
                )
            )
            dto = EvaluationSheetIdDto(uuid4())
            request_user = UserFactory()

            result = usecase.retrieve(request_user, dto)

            self.assertIsNotNone(result)
            self.assertEqual(result.own_weighted_total, 36)
            self.assertEqual(result.own_weighted_max, 60)
            self.assertEqual(result.manager_weighted_total, 32)
            self.assertEqual(result.manager_weighted_max, 40)
            self.assertEqual(len(result.own_category_scores), 1)
            self.assertEqual(len(result.manager_category_scores), 1)
            own_summary = result.own_category_scores[0]
            manager_summary = result.manager_category_scores[0]
            self.assertEqual(
                own_summary.category, EvaluationItemCategory.PERFORMANCE_RESULTS
            )
            self.assertEqual(own_summary.total, 3)
            self.assertEqual(own_summary.max_total, 5)
            self.assertEqual(own_summary.weighted_total, 36)
            self.assertEqual(own_summary.weighted_max, 60)
            self.assertEqual(
                manager_summary.category, EvaluationItemCategory.ATTITUDE_SKILLS
            )
            self.assertEqual(manager_summary.total, 4)
            self.assertEqual(manager_summary.max_total, 5)
            self.assertEqual(manager_summary.weighted_total, 32)
            self.assertEqual(manager_summary.weighted_max, 40)

    def test_list_by_employee_id(self) -> None:
        with self.subTest("従業員IDで一覧取得できること"):
            usecase = EvaluationSheetUsecase()
            employee_id = uuid4()
            own_score = EvaluationScoreRetrieveModelFactory(
                category=EvaluationItemCategory.PERFORMANCE_RESULTS,
                score=3,
            )
            manager_score = EvaluationScoreRetrieveModelFactory(
                category=EvaluationItemCategory.ATTITUDE_SKILLS,
                score=4,
            )
            expected = [
                EvaluationSheetRawModelFactory(
                    employee_uuid=employee_id,
                    self_evaluation_score=[own_score],
                    manager_evaluation_score=[manager_score],
                ),
                EvaluationSheetRawModelFactory(
                    employee_uuid=employee_id,
                    self_evaluation_score=[own_score],
                    manager_evaluation_score=[manager_score],
                ),
            ]
            usecase.evaluation_sheet_query_service.get_list_by_employee_id = MagicMock(
                return_value=expected
            )
            usecase.employee_repository.find_by_id = MagicMock(
                return_value=EmployeeFactory(uuid=employee_id)
            )
            usecase.evaluation_weight_policy_query_service.get_weights = MagicMock(
                side_effect=lambda _user,
                period_id,
                position: EvaluationWeightPolicyListModel(
                    period_uuid=period_id,
                    position=position,
                    weights=[
                        EvaluationWeightModel(
                            category=EvaluationItemCategory.PERFORMANCE_RESULTS,
                            weight=60,
                        ),
                        EvaluationWeightModel(
                            category=EvaluationItemCategory.ATTITUDE_SKILLS, weight=40
                        ),
                    ],
                )
            )
            dto = EvaluationSheetEmployeeIdDto(uuid4())
            request_user = UserFactory()

            result = usecase.list_by_employee_id(request_user, dto)

            self.assertEqual(len(result), 2)
            for sheet in result:
                self.assertIsNotNone(sheet.own_weighted_total)
                self.assertIsNotNone(sheet.manager_weighted_total)
                self.assertEqual(sheet.own_weighted_max, 60)
                self.assertEqual(sheet.manager_weighted_max, 40)

    def test_create(self) -> None:
        with self.subTest("すでに評価シートが存在する場合にエラーになること"):
            usecase = EvaluationSheetUsecase()
            usecase.evaluation_sheet_repository.get_by_employee_period = MagicMock(
                return_value=EvaluationSheetFactory()
            )
            dto = EvaluationSheetCreateDto(uuid4(), uuid4())
            request_user = UserFactory()

            with self.assertRaises(ValidationError) as e:
                usecase.create(request_user, dto)

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
            request_user = UserFactory(employee_uuid=employee_id)

            result = usecase.create(request_user, dto)

            self.assertEqual(result, created_sheet)

    def test_update_own(self) -> None:
        with self.subTest("評価シートが存在しない場合にエラーになること"):
            usecase = EvaluationSheetUsecase()
            usecase.evaluation_sheet_repository.find_by_id = MagicMock(
                return_value=None
            )
            dto = EvaluationSheetUpdateDto(uuid4(), [], True)
            request_user = UserFactory()

            with self.assertRaises(ValidationError) as e:
                usecase.update_own(request_user, dto)

            self.assertEqual(e.exception.detail, ["評価シートが存在しません。"])

        with self.subTest("更新者が一致しない場合にエラーになること"):
            usecase = EvaluationSheetUsecase()
            entity = EvaluationSheetFactory(employee_uuid=uuid4())
            usecase.evaluation_sheet_repository.find_by_id = MagicMock(
                return_value=entity
            )
            dto = EvaluationSheetUpdateDto(uuid4(), [], True)
            request_user = UserFactory(employee_uuid=uuid4())

            with self.assertRaises(ValidationError) as e:
                usecase.update_own(request_user, dto)

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
            dto = EvaluationSheetUpdateDto(uuid4(), [], True)
            request_user = UserFactory(employee_uuid=employee_id)

            with self.assertRaises(ValidationError) as e:
                usecase.update_own(request_user, dto)

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
                [
                    EvaluationSheetScoreDto(item_id1, 3),
                    EvaluationSheetScoreDto(item_id2, 4),
                ],
                False,
            )
            actor = UserFactory(employee_uuid=employee_id)

            result = usecase.update_own(actor, dto)

            self.assertIsNotNone(result)
            self.assertEqual(result.uuid, entity.uuid)
            self.assertEqual(result.employee_uuid, employee_id)
            self.assertEqual(result.own_status, EvaluationSheetStatusEnum.COMPLETED)
            self.assertEqual(result.own_scores[0].score, 3)
            self.assertEqual(result.own_scores[1].score, 4)

    def test_update_by_manager(self) -> None:
        with self.subTest("評価シートが存在しない場合にエラーになること"):
            usecase = EvaluationSheetUsecase()
            usecase.evaluation_sheet_repository.find_by_id = MagicMock(
                return_value=None
            )
            dto = EvaluationSheetUpdateDto(uuid4(), [], True)
            request_user = UserFactory()

            with self.assertRaises(ValidationError) as e:
                usecase.update_by_manager(request_user, dto)

            self.assertEqual(e.exception.detail, ["評価シートが存在しません。"])

        with self.subTest("評価対象の従業員が存在しない場合にエラーになること"):
            usecase = EvaluationSheetUsecase()
            employee_id = uuid4()
            entity = EvaluationSheetFactory(employee_uuid=employee_id)
            usecase.evaluation_sheet_repository.find_by_id = MagicMock(
                return_value=entity
            )
            usecase.employee_repository.find_by_id = MagicMock(return_value=None)
            dto = EvaluationSheetUpdateDto(uuid4(), [], True)
            request_user = UserFactory()

            with self.assertRaises(ValidationError) as e:
                usecase.update_by_manager(request_user, dto)

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
            dto = EvaluationSheetUpdateDto(uuid4(), [], True)
            request_user = UserFactory()

            with self.assertRaises(ValidationError) as e:
                usecase.update_by_manager(request_user, dto)

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
            dto = EvaluationSheetUpdateDto(uuid4(), [], True)
            request_user = UserFactory(employee_uuid=uuid4())

            with self.assertRaises(ValidationError) as e:
                usecase.update_by_manager(request_user, dto)

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
                [
                    EvaluationSheetScoreDto(item_id1, 3),
                    EvaluationSheetScoreDto(item_id2, 4),
                ],
                False,
            )
            request_user = UserFactory(employee_uuid=manager_id)

            result = usecase.update_by_manager(request_user, dto)

            self.assertIsNotNone(result)
            self.assertEqual(result.uuid, entity.uuid)
            self.assertEqual(result.employee_uuid, employee_id)
            self.assertEqual(
                result.manager_status, EvaluationSheetStatusEnum.COMPLETED
            )
            self.assertEqual(result.manager_scores[0].score, 3)
            self.assertEqual(result.manager_scores[1].score, 4)
