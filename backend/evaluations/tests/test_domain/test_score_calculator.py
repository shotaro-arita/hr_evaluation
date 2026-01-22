from evaluations.domain.evaluation_item.entity import EvaluationItemCategory
from evaluations.domain.evaluation_sheet.score_calculator import (
    calculate_weighted_score,
)
from evaluations.tests.utils.testcase import MyAPITestCase


class ScoreCalculatorTest(MyAPITestCase):
    def test_calculate_weighted_score(self) -> None:
        scores = [
            (EvaluationItemCategory.PERFORMANCE_RESULTS, 4),
            (EvaluationItemCategory.PERFORMANCE_RESULTS, 5),
            (EvaluationItemCategory.PERFORMANCE_RESULTS, 3),
            (EvaluationItemCategory.ATTITUDE_SKILLS, 2),
            (EvaluationItemCategory.ATTITUDE_SKILLS, 4),
        ]
        weight_map = {
            EvaluationItemCategory.PERFORMANCE_RESULTS: 60,
            EvaluationItemCategory.ATTITUDE_SKILLS: 40,
        }

        result = calculate_weighted_score(scores, weight_map)

        # 12/15 * 60 + 6/10 * 40 = 48 + 24 = 72
        self.assertEqual(result.weighted_total, 72)
        self.assertEqual(result.weighted_max, 100)

        summaries = {s.category: s for s in result.category_summaries}
        performance = summaries[EvaluationItemCategory.PERFORMANCE_RESULTS]
        attitude = summaries[EvaluationItemCategory.ATTITUDE_SKILLS]

        self.assertEqual(performance.total, 12)
        self.assertEqual(performance.max_total, 15)
        self.assertEqual(performance.weight, 60)
        self.assertEqual(performance.weighted_score, 48)

        self.assertEqual(attitude.total, 6)
        self.assertEqual(attitude.max_total, 10)
        self.assertEqual(attitude.weight, 40)
        self.assertEqual(attitude.weighted_score, 24)
