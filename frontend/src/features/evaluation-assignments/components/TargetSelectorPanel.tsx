import {
  Box,
  ButtonBase,
  Paper,
  Stack,
  Typography,
} from '@mui/material'
import type { EvaluationSheetStatus } from '../../../shared/types/enums'
import { getEvaluationSheetStatusLabel } from '../../../shared/types/enums'

type TargetStatus = {
  own_status: EvaluationSheetStatus
  manager_status: EvaluationSheetStatus
} | null

type TargetOption = {
  employeeId: string
  label: string
  status: TargetStatus
  isSelf?: boolean
}

type Props = {
  targets: TargetOption[]
  selectedEmployeeId: string
  helperText: string
  loading: boolean
  onChange: (value: string) => void
}

export const TargetSelectorPanel = ({
  targets,
  selectedEmployeeId,
  helperText,
  loading,
  onChange,
}: Props) => {
  const getStatusText = (status?: EvaluationSheetStatus) =>
    status ? getEvaluationSheetStatusLabel(status) : '未作成'

  return (
    <Paper
      elevation={0}
      sx={{ p: 3, border: '1px solid', borderColor: 'divider' }}
    >
      <Typography variant="h2">評価対象</Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
        一覧を確認したい対象者を選択します。
      </Typography>
      <Typography variant="caption" color="text.secondary" sx={{ mt: 1 }}>
        {loading ? 'ステータスを取得中です...' : helperText}
      </Typography>
      {targets.length === 0 ? (
        <Typography sx={{ mt: 2 }} color="text.secondary">
          評価対象がありません。
        </Typography>
      ) : (
        <Box
          sx={{
            mt: 2,
            display: 'grid',
            gap: 2,
            gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
          }}
        >
          {targets.map((target) => {
            const isSelected = selectedEmployeeId === target.employeeId
            return (
              <ButtonBase
                key={target.employeeId}
                onClick={() => onChange(target.employeeId)}
                sx={{ textAlign: 'left' }}
              >
                <Paper
                  elevation={0}
                  sx={{
                    p: 2,
                    width: '100%',
                    border: '1px solid',
                    borderColor: isSelected ? 'primary.main' : 'divider',
                  }}
                >
                  <Stack spacing={0.5}>
                    <Typography fontWeight={600}>{target.label}</Typography>
                    {target.isSelf ? (
                      <Typography variant="caption" color="text.secondary">
                        自分
                      </Typography>
                    ) : null}
                    <Typography variant="body2" color="text.secondary">
                      自分: {getStatusText(target.status?.own_status)}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      評価者: {getStatusText(target.status?.manager_status)}
                    </Typography>
                  </Stack>
                </Paper>
              </ButtonBase>
            )
          })}
        </Box>
      )}
    </Paper>
  )
}
