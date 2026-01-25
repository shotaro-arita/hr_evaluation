import {
  Box,
  Button,
  Paper,
  Stack,
  Tooltip,
  Typography,
} from '@mui/material'
import type { EvaluationItemCategory } from '../../../shared/types/enums'
import {
  getEvaluationItemCategoryLabel,
  getEvaluationSheetStatusLabel,
} from '../../../shared/types/enums'
import type { CategoryScoreSummary, EvaluationSheet, ScoreItem } from '../types'

type Props = {
  selectedSheet: EvaluationSheet | null
  ownScores: ScoreItem[]
  managerScores: ScoreItem[]
  ownDraft: Record<string, string>
  managerDraft: Record<string, string>
  canEditOwn: boolean
  canEditManager: boolean
  loading: boolean
  onSaveOwnTemp: () => void
  onSaveOwnFinal: () => void
  onSaveManagerTemp: () => void
  onSaveManagerFinal: () => void
  onOwnScoreChange: (itemId: string, value: string) => void
  onManagerScoreChange: (itemId: string, value: string) => void
}

export const SheetDetailPanel = ({
  selectedSheet,
  ownScores,
  managerScores,
  ownDraft,
  managerDraft,
  canEditOwn,
  canEditManager,
  loading,
  onSaveOwnTemp,
  onSaveOwnFinal,
  onSaveManagerTemp,
  onSaveManagerFinal,
  onOwnScoreChange,
  onManagerScoreChange,
}: Props) => {
  const isOwnCompleted = selectedSheet?.own_status === 'COMPLETED'
  const isManagerCompleted = selectedSheet?.manager_status === 'COMPLETED'

  const renderScoreRow = (
    item: ScoreItem,
    draft: Record<string, string>,
    canEdit: boolean,
    onChange: (itemId: string, value: string) => void
  ) => {
    const selectedValue = draft[item.item_uuid]
    return (
      <Stack direction="row" spacing={1} alignItems="center">
        {[1, 2, 3, 4, 5].map((score) => {
          const criteriaKey = `criteria_${score}` as const
          const criteriaText = item[criteriaKey]
          const isSelected = selectedValue === String(score)
          return (
            <Tooltip key={score} title={criteriaText} arrow placement="top">
              <span>
                <Button
                  variant={isSelected ? 'contained' : 'outlined'}
                  size="small"
                  onClick={() => onChange(item.item_uuid, String(score))}
                  disabled={!canEdit || loading}
                >
                  {score}
                </Button>
              </span>
            </Tooltip>
          )
        })}
      </Stack>
    )
  }

  const buildCategoryTotals = (
    scores: ScoreItem[],
    draft: Record<string, string>
  ) =>
    scores.reduce<Record<string, { total: number; max: number }>>((acc, item) => {
      const key = item.category
      const value = draft[item.item_uuid]
      const parsed = value ? Number(value) : 0
      if (!acc[key]) {
        acc[key] = { total: 0, max: 0 }
      }
      acc[key].total += Number.isNaN(parsed) ? 0 : parsed
      acc[key].max += 5
      return acc
    }, {})

  const formatScore = (value: number | null | undefined, max?: number | null) => {
    if (value === null || value === undefined || max === null || max === undefined) {
      return '-'
    }
    return `${value} / ${max}`
  }

  const getCategorySummary = (
    summaries: CategoryScoreSummary[] | undefined,
    category: EvaluationItemCategory
  ) => summaries?.find((summary) => summary.category === category)

  const renderScoreGroups = () => {
    const groupedScores = ownScores.reduce<Record<string, ScoreItem[]>>(
      (acc, item) => {
        if (!acc[item.category]) {
          acc[item.category] = []
        }
        acc[item.category].push(item)
        return acc
      },
      {}
    )
    const managerScoreMap = new Map(
      managerScores.map((item) => [item.item_uuid, item])
    )
    const ownTotals = buildCategoryTotals(ownScores, ownDraft)
    const managerTotals = buildCategoryTotals(managerScores, managerDraft)
    return Object.entries(groupedScores).map(([category, items]) => (
      <Stack key={category} spacing={1.5}>
        <Stack
          direction={{ xs: 'column', sm: 'row' }}
          spacing={2}
          alignItems={{ xs: 'flex-start', sm: 'center' }}
          justifyContent="space-between"
        >
          <Typography variant="h2">
            {getEvaluationItemCategoryLabel(category as EvaluationItemCategory)}
          </Typography>
          <Stack spacing={0.5} alignItems={{ xs: 'flex-start', sm: 'flex-end' }}>
            <Typography variant="caption" color="text.secondary">
              合計得点{' '}
              {formatScore(ownTotals[category]?.total, ownTotals[category]?.max)} /
              考課割合{' '}
              {formatScore(
                getCategorySummary(
                  selectedSheet?.own_category_scores,
                  category as EvaluationItemCategory
                )?.weighted_total,
                getCategorySummary(
                  selectedSheet?.own_category_scores,
                  category as EvaluationItemCategory
                )?.weighted_max
              )}
            </Typography>
            <Typography variant="caption" color="text.secondary">
              合計得点{' '}
              {formatScore(
                managerTotals[category]?.total,
                managerTotals[category]?.max
              )}{' '}
              / 考課割合{' '}
              {formatScore(
                getCategorySummary(
                  selectedSheet?.manager_category_scores,
                  category as EvaluationItemCategory
                )?.weighted_total,
                getCategorySummary(
                  selectedSheet?.manager_category_scores,
                  category as EvaluationItemCategory
                )?.weighted_max
              )}
            </Typography>
          </Stack>
        </Stack>
        {items.map((item) => {
          const managerItem = managerScoreMap.get(item.item_uuid)
          return (
            <Paper
              key={item.item_uuid}
              elevation={0}
              sx={{ p: 2, border: '1px solid', borderColor: 'divider' }}
            >
              <Stack spacing={1.5}>
                <Stack
                  direction={{ xs: 'column', md: 'row' }}
                  spacing={2}
                  alignItems={{ xs: 'flex-start', md: 'center' }}
                  justifyContent="space-between"
                >
                  <Tooltip title={item.description} arrow placement="top-start">
                    <Box>
                      <Typography fontWeight={600}>{item.title}</Typography>
                    </Box>
                  </Tooltip>
                  <Stack spacing={1} alignItems="flex-end">
                    {renderScoreRow(
                      item,
                      ownDraft,
                      canEditOwn && !isOwnCompleted,
                      onOwnScoreChange
                    )}
                    {managerItem ? (
                      renderScoreRow(
                        managerItem,
                        managerDraft,
                        canEditManager && !isManagerCompleted,
                        onManagerScoreChange
                      )
                    ) : (
                      <Typography variant="caption" color="text.secondary">
                        評価者評価はまだありません。
                      </Typography>
                    )}
                  </Stack>
                </Stack>
              </Stack>
            </Paper>
          )
        })}
      </Stack>
    ))
  }

  const sumDraftScores = (scores: ScoreItem[], draft: Record<string, string>) =>
    scores.reduce((total, item) => {
      const value = draft[item.item_uuid]
      if (!value) return total
      const parsed = Number(value)
      return Number.isNaN(parsed) ? total : total + parsed
    }, 0)

  const renderTotalScore = (
    label: string,
    scores: ScoreItem[],
    draft: Record<string, string>,
    weightedTotal: number | null | undefined,
    weightedMax: number | null | undefined
  ) => {
    const total = sumDraftScores(scores, draft)
    const max = scores.length * 5
    return (
      <Stack spacing={0.5}>
        <Typography variant="body2" color="text.secondary">
          {label} 合計得点 {total} / {max}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          {label} 考課割合 {formatScore(weightedTotal, weightedMax)}
        </Typography>
      </Stack>
    )
  }

  return (
    <Paper
      elevation={0}
      sx={{ p: 3, border: '1px solid', borderColor: 'divider' }}
    >
      <Stack
        direction={{ xs: 'column', sm: 'row' }}
        spacing={2}
        alignItems={{ xs: 'flex-start', sm: 'center' }}
        justifyContent="space-between"
      >
        <Box>
          <Typography variant="h2">評価シート詳細</Typography>
          <Typography variant="body2" color="text.secondary">
            {selectedSheet
              ? `${selectedSheet.employee_name} / ${selectedSheet.period_name}`
              : '一覧からシートを選択してください'}
          </Typography>
          {selectedSheet ? (
            <Typography variant="body2" color="text.secondary">
              本人: {getEvaluationSheetStatusLabel(selectedSheet.own_status)} / 評価者:{' '}
              {getEvaluationSheetStatusLabel(selectedSheet.manager_status)}
            </Typography>
          ) : null}
        </Box>
        {selectedSheet ? (
          <Stack spacing={1} alignItems={{ xs: 'flex-start', sm: 'flex-end' }}>
            <Stack direction="row" spacing={1}>
              <Typography variant="caption" color="text.secondary">
                上段: 本人評価 / 下段: 評価者評価
              </Typography>
            </Stack>
            <Stack direction="row" spacing={2}>
              {renderTotalScore(
                '本人合計',
                ownScores,
                ownDraft,
                selectedSheet?.own_weighted_total,
                selectedSheet?.own_weighted_max
              )}
              {renderTotalScore(
                '評価者合計',
                managerScores,
                managerDraft,
                selectedSheet?.manager_weighted_total,
                selectedSheet?.manager_weighted_max
              )}
            </Stack>
            <Stack direction="row" spacing={2}>
              {canEditOwn ? (
                <Stack direction="row" spacing={1}>
                  <Button
                    variant="outlined"
                    disabled={loading || isOwnCompleted}
                    onClick={onSaveOwnTemp}
                  >
                    下書き保存
                  </Button>
                  <Button
                    variant="contained"
                    disabled={loading || isOwnCompleted}
                    onClick={onSaveOwnFinal}
                  >
                    提出する
                  </Button>
                </Stack>
              ) : null}
              {canEditManager ? (
                <Stack direction="row" spacing={1}>
                  <Button
                    variant="outlined"
                    disabled={loading || isManagerCompleted}
                    onClick={onSaveManagerTemp}
                  >
                    下書き保存
                  </Button>
                  <Button
                    variant="contained"
                    disabled={loading || isManagerCompleted}
                    onClick={onSaveManagerFinal}
                  >
                    提出する
                  </Button>
                </Stack>
              ) : null}
            </Stack>
          </Stack>
        ) : null}
      </Stack>
      {selectedSheet ? (
        <Stack spacing={2} sx={{ mt: 2 }}>
          {renderScoreGroups()}
        </Stack>
      ) : (
        <Typography sx={{ mt: 2 }} color="text.secondary">
          詳細データはここに表示されます。
        </Typography>
      )}
    </Paper>
  )
}
