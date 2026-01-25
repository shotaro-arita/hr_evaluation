from evaluations.tests.utils.entity_factory import (
    EvaluationSheetFactory,
    EvaluationSheetScoreFactory,
)
from evaluations.tests.utils.testcase import MyAPITestCase
from uuid import uuid4
from rest_framework.exceptions import ValidationError
from evaluations.domain.evaluation_sheet.entity import EvaluationSheetStatusEnum


class EvaluationSheetTest(MyAPITestCase):
    def test_check_update_own(self) -> None:
        with self.subTest("id不一致でテストがエラーが発生すること。"):
            actor_employee_id = uuid4()
            entity = EvaluationSheetFactory()

            with self.assertRaises(ValidationError) as e:
                entity.check_update_own(actor_employee_id)

            self.assertEqual(
                e.exception.detail, ["更新者と評価シートの対象者が一致していません。"]
            )

    def test_update_sheet_score_from_dict(self) -> None:
        with self.subTest("更新しようとしている評価項目が不一致"):
            sheet_scores = [EvaluationSheetScoreFactory()]
            score_dict = {uuid4(): None}
            entity = EvaluationSheetFactory()

            with self.assertRaises(ValidationError) as e:
                entity._update_sheet_score_from_dict(sheet_scores, score_dict, True)

            self.assertEqual(
                e.exception.detail,
                ["更新しようとしている評価項目が定義と一致しません。"],
            )

        with self.subTest("正常に更新できること"):
            sheet_score_id1 = uuid4()
            sheet_score_id2 = uuid4()
            sheet_scores = [
                EvaluationSheetScoreFactory(evaluation_item_uuid=sheet_score_id1),
                EvaluationSheetScoreFactory(evaluation_item_uuid=sheet_score_id2),
            ]
            score_dict = {sheet_score_id1: 1, sheet_score_id2: 2}
            entity = EvaluationSheetFactory()

            result = entity._update_sheet_score_from_dict(
                sheet_scores, score_dict, False
            )

            self.assertEqual(len(result), 2)
            self.assertEqual(result[0].score, 1)
            self.assertEqual(result[1].score, 2)

    def test_save_temporary_own_score(self) -> None:
        with self.subTest("下書きとして保存できること"):
            sheet_score_id1 = uuid4()
            sheet_score_id2 = uuid4()
            own_scores = [
                EvaluationSheetScoreFactory(evaluation_item_uuid=sheet_score_id1),
                EvaluationSheetScoreFactory(evaluation_item_uuid=sheet_score_id2),
            ]
            entity = EvaluationSheetFactory(own_scores=own_scores)
            score_dict = {sheet_score_id1: 3, sheet_score_id2: 5}

            result = entity.save_temporary_own_score(score_dict)

            self.assertEqual(
                result.own_status, EvaluationSheetStatusEnum.DRAFT
            )
            self.assertEqual(result.own_scores[0].score, 3)
            self.assertEqual(result.own_scores[1].score, 5)

        with self.subTest("完了済みは下書きに更新できないこと"):
            sheet_score_id = uuid4()
            own_scores = [
                EvaluationSheetScoreFactory(evaluation_item_uuid=sheet_score_id),
            ]
            entity = EvaluationSheetFactory(
                own_scores=own_scores,
                own_status=EvaluationSheetStatusEnum.COMPLETED,
            )
            score_dict = {sheet_score_id: 3}

            with self.assertRaises(ValidationError) as e:
                entity.save_temporary_own_score(score_dict)

            self.assertEqual(
                e.exception.detail, ["完了済みの自己評価は下書きに更新できません。"]
            )

    def test_complete_own_score(self) -> None:
        with self.subTest("スコア未入力でエラーになること"):
            sheet_score_id = uuid4()
            own_scores = [
                EvaluationSheetScoreFactory(evaluation_item_uuid=sheet_score_id),
            ]
            entity = EvaluationSheetFactory(own_scores=own_scores)
            score_dict = {sheet_score_id: None}

            with self.assertRaises(ValidationError) as e:
                entity.complete_own_score(score_dict)

            self.assertEqual(e.exception.detail, ["スコアが入力されていません。"])

        with self.subTest("完了として保存できること"):
            sheet_score_id1 = uuid4()
            sheet_score_id2 = uuid4()
            own_scores = [
                EvaluationSheetScoreFactory(evaluation_item_uuid=sheet_score_id1),
                EvaluationSheetScoreFactory(evaluation_item_uuid=sheet_score_id2),
            ]
            entity = EvaluationSheetFactory(own_scores=own_scores)
            score_dict = {sheet_score_id1: 1, sheet_score_id2: 4}

            result = entity.complete_own_score(score_dict)

            self.assertEqual(result.own_status, EvaluationSheetStatusEnum.COMPLETED)
            self.assertEqual(result.own_scores[0].score, 1)
            self.assertEqual(result.own_scores[1].score, 4)

    def test_save_temporary_manager_score(self) -> None:
        with self.subTest("下書きとして保存できること"):
            sheet_score_id1 = uuid4()
            sheet_score_id2 = uuid4()
            manager_scores = [
                EvaluationSheetScoreFactory(evaluation_item_uuid=sheet_score_id1),
                EvaluationSheetScoreFactory(evaluation_item_uuid=sheet_score_id2),
            ]
            entity = EvaluationSheetFactory(manager_scores=manager_scores)
            score_dict = {sheet_score_id1: None, sheet_score_id2: 2}

            result = entity.save_temporary_manager_score(score_dict)

            self.assertEqual(
                result.manager_status, EvaluationSheetStatusEnum.DRAFT
            )
            self.assertIsNone(result.manager_scores[0].score)
            self.assertEqual(result.manager_scores[1].score, 2)

        with self.subTest("完了済みは下書きに更新できないこと"):
            sheet_score_id = uuid4()
            manager_scores = [
                EvaluationSheetScoreFactory(evaluation_item_uuid=sheet_score_id),
            ]
            entity = EvaluationSheetFactory(
                manager_scores=manager_scores,
                manager_status=EvaluationSheetStatusEnum.COMPLETED,
            )
            score_dict = {sheet_score_id: 2}

            with self.assertRaises(ValidationError) as e:
                entity.save_temporary_manager_score(score_dict)

            self.assertEqual(
                e.exception.detail, ["完了済みの管理者評価は下書きに更新できません。"]
            )

    def test_update_manager_score(self) -> None:
        with self.subTest("スコア未入力でエラーになること"):
            sheet_score_id = uuid4()
            manager_scores = [
                EvaluationSheetScoreFactory(evaluation_item_uuid=sheet_score_id),
            ]
            entity = EvaluationSheetFactory(manager_scores=manager_scores)
            score_dict = {sheet_score_id: None}

            with self.assertRaises(ValidationError) as e:
                entity.update_manager_score(score_dict)

            self.assertEqual(e.exception.detail, ["スコアが入力されていません。"])

        with self.subTest("完了として保存できること"):
            sheet_score_id1 = uuid4()
            sheet_score_id2 = uuid4()
            manager_scores = [
                EvaluationSheetScoreFactory(evaluation_item_uuid=sheet_score_id1),
                EvaluationSheetScoreFactory(evaluation_item_uuid=sheet_score_id2),
            ]
            entity = EvaluationSheetFactory(manager_scores=manager_scores)
            score_dict = {sheet_score_id1: 2, sheet_score_id2: 5}

            result = entity.update_manager_score(score_dict)

            self.assertEqual(
                result.manager_status, EvaluationSheetStatusEnum.COMPLETED
            )
            self.assertEqual(result.manager_scores[0].score, 2)
            self.assertEqual(result.manager_scores[1].score, 5)
