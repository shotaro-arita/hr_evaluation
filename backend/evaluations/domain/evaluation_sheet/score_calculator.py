from collections.abc import Iterable
from dataclasses import dataclass

from evaluations.domain.evaluation_item.entity import EvaluationItemCategory


@dataclass(frozen=True)
class CategoryScoreSummary:
    category: EvaluationItemCategory
    total: int
    max_total: int
    weight: int | None
    weighted_score: int | None


@dataclass(frozen=True)
class WeightedScoreResult:
    weighted_total: int
    weighted_max: int
    category_summaries: list[CategoryScoreSummary]


def _round_half_up(value: float) -> int:
    return int(value + 0.5)


def calculate_weighted_score(
    scores: Iterable[tuple[EvaluationItemCategory, int | None]],
    weight_map: dict[EvaluationItemCategory, int],
) -> WeightedScoreResult:
    totals: dict[EvaluationItemCategory, list[int]] = {}
    for category, score in scores:
        if category not in totals:
            totals[category] = []
        totals[category].append(score or 0)

    summaries: list[CategoryScoreSummary] = []
    weighted_total = 0
    weighted_max = 0
    for category, values in totals.items():
        total = sum(values)
        max_total = len(values) * 5
        weight = weight_map.get(category)
        weighted_score = None
        if weight is not None and max_total > 0:
            # カテゴリのトータルごとに重み付けして四捨五入
            weighted_score = _round_half_up((total / max_total) * weight)
            weighted_total += weighted_score
            weighted_max += weight
        summaries.append(
            CategoryScoreSummary(
                category=category,
                total=total,
                max_total=max_total,
                weight=weight,
                weighted_score=weighted_score,
            )
        )

    return WeightedScoreResult(
        weighted_total=weighted_total,
        weighted_max=weighted_max,
        category_summaries=summaries,
    )
