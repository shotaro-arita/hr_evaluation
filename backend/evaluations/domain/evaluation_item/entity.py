from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID


class EvaluationItemCategory(str, Enum):
    PERFORMANCE_RESULTS = "PERFORMANCE_RESULTS"
    ATTITUDE_SKILLS = "ATTITUDE_SKILLS"
    PROJECT_MANAGEMENT = "PROJECT_MANAGEMENT"
    TECHNICAL_SOFTWARE = "TECHNICAL_SOFTWARE"
    TECHNICAL_INFRASTRUCTURE = "TECHNICAL_INFRASTRUCTURE"
    TECHNICAL_MAINTENANCE = "TECHNICAL_MAINTENANCE"

    @property
    def text(self) -> str:
        if self.value == EvaluationItemCategory.PERFORMANCE_RESULTS:
            return "成果・業績評価"
        elif self.value == EvaluationItemCategory.ATTITUDE_SKILLS:
            return "態度・能力評価"
        elif self.value == EvaluationItemCategory.PROJECT_MANAGEMENT:
            return "プロジェクト管理技術評価"
        elif self.value == EvaluationItemCategory.TECHNICAL_SOFTWARE:
            return "技術評価（ソフト開発）"
        elif self.value == EvaluationItemCategory.TECHNICAL_INFRASTRUCTURE:
            return "技術評価（インフラ構築）"
        elif self.value == EvaluationItemCategory.TECHNICAL_MAINTENANCE:
            return "技術評価（保守運用）"
        else:
            raise ValueError("無効な評価項目カテゴリです。")


@dataclass(frozen=True)
class EvaluationItem:
    uuid: UUID
    title: str
    category: EvaluationItemCategory
    description: str

    criteria_1: str
    criteria_2: str
    criteria_3: str
    criteria_4: str
    criteria_5: str

    created_at: datetime
    updated_at: datetime
