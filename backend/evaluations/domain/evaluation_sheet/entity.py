from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from rest_framework.exceptions import ValidationError


class EvaluationSheetStatusEnum(str, Enum):
    PENDING = "PENDING"
    DRAFT = "DRAFT"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

    @property
    def text(self) -> str:
        if self.value == EvaluationSheetStatusEnum.PENDING:
            return "未完了"
        elif self.value == EvaluationSheetStatusEnum.DRAFT:
            return "下書き"
        elif self.value == EvaluationSheetStatusEnum.COMPLETED:
            return "完了"
        elif self.value == EvaluationSheetStatusEnum.CANCELLED:
            return "キャンセル"
        else:
            raise ValueError("無効な役割です。")

    @classmethod
    def choices(cls) -> list[tuple[str, str]]:
        return [(s.value, s.text) for s in cls]


@dataclass(frozen=True)
class EvaluationSheet:
    uuid: UUID

    period_uuid: UUID
    employee_uuid: UUID

    own_scores: list["EvaluationSheetScore"]
    manager_scores: list["EvaluationSheetScore"]

    own_status: EvaluationSheetStatusEnum
    manager_status: EvaluationSheetStatusEnum

    created_at: datetime | None
    updated_at: datetime | None

    @classmethod
    def initialize(
        cls, period_uuid: UUID, employee_uuid: UUID, evaluation_item_ids: list[UUID]
    ) -> "EvaluationSheet":
        uuid = uuid4()
        own_scores = [
            EvaluationSheetScore.init(item_uuid) for item_uuid in evaluation_item_ids
        ]
        manager_scores = [
            EvaluationSheetScore.init(item_uuid) for item_uuid in evaluation_item_ids
        ]
        return cls(
            uuid=uuid,
            period_uuid=period_uuid,
            employee_uuid=employee_uuid,
            own_scores=own_scores,
            manager_scores=manager_scores,
            own_status=EvaluationSheetStatusEnum.PENDING,
            manager_status=EvaluationSheetStatusEnum.PENDING,
            created_at=None,
            updated_at=None,
        )

    def check_update_own(self, actor_employee_uuid: UUID) -> "EvaluationSheet":
        if self.employee_uuid != actor_employee_uuid:
            raise ValidationError("更新者と評価シートの対象者が一致していません。")
        return self

    def _update_sheet_score_from_dict(
        self,
        sheet_scores: list["EvaluationSheetScore"],
        score_dict: dict[UUID, int | None],
        is_temporary: bool,
    ) -> list["EvaluationSheetScore"]:
        sheet_item_ids = set([s.evaluation_item_uuid for s in sheet_scores])
        new_item_ids = set(score_dict.keys())
        if sheet_item_ids != new_item_ids:
            raise ValidationError("更新しようとしている評価項目が定義と一致しません。")

        new_scores = [
            sheet_score.update_score(
                score_dict[sheet_score.evaluation_item_uuid], is_temporary
            )
            for sheet_score in sheet_scores
        ]
        return new_scores

    def save_temporary_own_score(
        self, own_evaluation_score_dict: dict[UUID, int | None]
    ) -> "EvaluationSheet":
        # TODO 評価ステータスの遷移
        new_scores = self._update_sheet_score_from_dict(
            self.own_scores, own_evaluation_score_dict, True
        )
        object.__setattr__(self, "own_scores", new_scores)
        object.__setattr__(
            self, "own_status", EvaluationSheetStatusEnum.DRAFT
        )
        return self

    def complete_own_score(
        self, own_evaluation_score_dict: dict[UUID, int | None]
    ) -> "EvaluationSheet":
        new_scores = self._update_sheet_score_from_dict(
            self.own_scores, own_evaluation_score_dict, False
        )
        object.__setattr__(self, "own_scores", new_scores)
        object.__setattr__(self, "own_status", EvaluationSheetStatusEnum.COMPLETED)
        return self

    def save_temporary_manager_score(
        self, manager_evaluation_score_dict: dict[UUID, int | None]
    ) -> "EvaluationSheet":
        # TODO 自己評価前にも管理者は評価できる？
        new_scores = self._update_sheet_score_from_dict(
            self.manager_scores, manager_evaluation_score_dict, True
        )
        object.__setattr__(self, "manager_scores", new_scores)
        object.__setattr__(
            self, "manager_status", EvaluationSheetStatusEnum.DRAFT
        )
        return self

    def update_manager_score(
        self, manager_evaluation_score_dict: dict[UUID, int | None]
    ) -> "EvaluationSheet":
        # TODO 自己評価前にも管理者は評価できる？
        new_scores = self._update_sheet_score_from_dict(
            self.manager_scores, manager_evaluation_score_dict, False
        )
        object.__setattr__(self, "manager_scores", new_scores)
        object.__setattr__(self, "manager_status", EvaluationSheetStatusEnum.COMPLETED)
        return self


@dataclass(frozen=True)
class EvaluationSheetScore:
    # TODO そもそもクラス自体を自分と管理者評価で分けるべきか？
    # 管理者評価でルールが変わる等あれば分けるべきだが、今はないから良い。
    uuid: UUID
    evaluation_item_uuid: UUID
    score: int | None
    created_at: datetime | None
    updated_at: datetime | None

    @classmethod
    def init(cls, evaluation_item_uuid: UUID) -> "EvaluationSheetScore":
        uuid = uuid4()
        return cls(
            uuid=uuid,
            evaluation_item_uuid=evaluation_item_uuid,
            score=None,
            created_at=None,
            updated_at=None,
        )

    def validate_score(self, score: int | None) -> None:
        if score is None:
            return
        if not 1 <= score <= 5:
            raise ValidationError("スコアは1~5で入力してください。")

    def update_score(
        self, score: int | None, is_temporary: bool
    ) -> "EvaluationSheetScore":
        if not is_temporary and score is None:
            raise ValidationError("スコアが入力されていません。")
        self.validate_score(score)
        object.__setattr__(self, "score", score)
        return self
