from rest_framework_dataclasses.serializers import DataclassSerializer

from evaluations.usecase.evaluation_sheet.dto import (
    EvaluationSheetCreateDto,
    EvaluationSheetEmployeeIdDto,
    EvaluationSheetIdDto,
    EvaluationSheetScoreDto,
    EvaluationSheetUpdateDto,
)


class EvaluationSheetIdDtoSerializer(DataclassSerializer[EvaluationSheetIdDto]):
    class Meta:
        dataclass = EvaluationSheetIdDto


class EvaluationSheetEmployeeIdDtoSerializer(
    DataclassSerializer[EvaluationSheetEmployeeIdDto]
):
    class Meta:
        dataclass = EvaluationSheetEmployeeIdDto


class EvaluationSheetCreateDtoSerializer(DataclassSerializer[EvaluationSheetCreateDto]):
    class Meta:
        dataclass = EvaluationSheetCreateDto


class EvaluationSheetScoreDtoSerializer(DataclassSerializer[EvaluationSheetScoreDto]):
    class Meta:
        dataclass = EvaluationSheetScoreDto


class EvaluationSheetUpdateDtoSerializer(DataclassSerializer[EvaluationSheetUpdateDto]):
    sheet_scores = EvaluationSheetScoreDtoSerializer(many=True)

    class Meta:
        dataclass = EvaluationSheetUpdateDto
