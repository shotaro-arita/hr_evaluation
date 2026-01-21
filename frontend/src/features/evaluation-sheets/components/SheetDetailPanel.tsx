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
import type { EvaluationSheet, ScoreItem } from '../types'

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
    return Object.entries(groupedScores).map(([category, items]) => (
      <Stack key={category} spacing={1.5}>
        <Typography variant="h2">
          {getEvaluationItemCategoryLabel(category as EvaluationItemCategory)}
        </Typography>
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
                    {renderScoreRow(item, ownDraft, canEditOwn, onOwnScoreChange)}
                    {managerItem ? (
                      renderScoreRow(
                        managerItem,
                        managerDraft,
                        canEditManager,
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
              {canEditOwn ? (
                <Stack direction="row" spacing={1}>
                  <Button
                    variant="outlined"
                    disabled={loading}
                    onClick={onSaveOwnTemp}
                  >
                    下書き保存
                  </Button>
                  <Button
                    variant="contained"
                    disabled={loading}
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
                    disabled={loading}
                    onClick={onSaveManagerTemp}
                  >
                    下書き保存
                  </Button>
                  <Button
                    variant="contained"
                    disabled={loading}
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
