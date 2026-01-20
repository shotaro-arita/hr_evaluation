import {
  Box,
  Button,
  Paper,
  Stack,
  Tooltip,
  Typography,
} from '@mui/material'
import { useMemo } from 'react'
import type { EvaluationItemCategory } from '../../../shared/types/enums'
import { getEvaluationItemCategoryLabel } from '../../../shared/types/enums'
import type { EvaluationSheet, ScoreItem } from '../types'

type Props = {
  selectedSheet: EvaluationSheet | null
  editableScores: ScoreItem[]
  scoreDraft: Record<string, string>
  canEdit: boolean
  loading: boolean
  onSaveTemp: () => void
  onSaveFinal: () => void
  onScoreChange: (itemId: string, value: string) => void
}

export const SheetDetailPanel = ({
  selectedSheet,
  editableScores,
  scoreDraft,
  canEdit,
  loading,
  onSaveTemp,
  onSaveFinal,
  onScoreChange,
}: Props) => {
  const groupedScores = useMemo(() => {
    return editableScores.reduce<Record<string, ScoreItem[]>>((acc, item) => {
      if (!acc[item.category]) {
        acc[item.category] = []
      }
      acc[item.category].push(item)
      return acc
    }, {})
  }, [editableScores])

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
        </Box>
        {selectedSheet && (
          <Stack direction="row" spacing={1}>
            <Button
              variant="outlined"
              disabled={!canEdit || loading}
              onClick={onSaveTemp}
            >
              下書き保存
            </Button>
            <Button
              variant="contained"
              disabled={!canEdit || loading}
              onClick={onSaveFinal}
            >
              提出する
            </Button>
          </Stack>
        )}
      </Stack>
      {selectedSheet ? (
        <Stack spacing={3} sx={{ mt: 2 }}>
          {Object.entries(groupedScores).map(([category, items]) => (
            <Stack key={category} spacing={1.5}>
              <Typography variant="h2">
                {getEvaluationItemCategoryLabel(
                  category as EvaluationItemCategory
                )}
              </Typography>
              {items.map((item) => (
                <Paper
                  key={item.item_uuid}
                  elevation={0}
                  sx={{ p: 2, border: '1px solid', borderColor: 'divider' }}
                >
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
                    <Stack direction="row" spacing={1}>
                      {[1, 2, 3, 4, 5].map((score) => {
                        const criteriaKey = `criteria_${score}` as const
                        const criteriaText = item[criteriaKey]
                        const isSelected =
                          scoreDraft[item.item_uuid] === String(score)
                        return (
                          <Tooltip
                            key={score}
                            title={criteriaText}
                            arrow
                            placement="top"
                          >
                            <span>
                              <Button
                                variant={isSelected ? 'contained' : 'outlined'}
                                size="small"
                                onClick={() =>
                                  onScoreChange(item.item_uuid, String(score))
                                }
                                disabled={!canEdit || loading}
                              >
                                {score}
                              </Button>
                            </span>
                          </Tooltip>
                        )
                      })}
                    </Stack>
                  </Stack>
                </Paper>
              ))}
            </Stack>
          ))}
        </Stack>
      ) : (
        <Typography sx={{ mt: 2 }} color="text.secondary">
          詳細データはここに表示されます。
        </Typography>
      )}
    </Paper>
  )
}
