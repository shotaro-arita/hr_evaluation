import {
  Box,
  Button,
  ButtonBase,
  Paper,
  Stack,
  Typography,
} from '@mui/material'
import type { EvaluationSheet } from '../types'
import { getEvaluationSheetStatusLabel } from '../../../shared/types/enums'
import { formatDateTime } from '../../../shared/lib/date'

type Props = {
  sheets: EvaluationSheet[]
  selectedSheetId: string | null
  loading: boolean
  onReload: () => void
  onCreate: () => void
  canCreate: boolean
  onSelect: (sheetId: string) => void
  selectedEmployeeId: string
}

export const SheetListPanel = ({
  sheets,
  selectedSheetId,
  loading,
  onReload,
  onCreate,
  canCreate,
  onSelect,
  selectedEmployeeId,
}: Props) => {
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
          <Typography variant="h2">評価シート一覧</Typography>
          <Typography variant="body2" color="text.secondary">
            {selectedEmployeeId
              ? `${sheets.length} 件のシート`
              : '対象者を選択してください'}
          </Typography>
        </Box>
        <Stack direction="row" spacing={1}>
          <Button
            variant="contained"
            onClick={onCreate}
            disabled={!canCreate}
          >
            今期の評価シートを作成
          </Button>
          <Button
            variant="outlined"
            onClick={onReload}
            disabled={loading || !selectedEmployeeId}
          >
            再読み込み
          </Button>
        </Stack>
      </Stack>
      {sheets.length === 0 ? (
        <Typography sx={{ mt: 2 }} color="text.secondary">
          評価シートがありません。
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
          {sheets.map((sheet) => (
            <ButtonBase
              key={sheet.uuid}
              onClick={() => onSelect(sheet.uuid)}
              sx={{ textAlign: 'left' }}
            >
              <Paper
                elevation={0}
                sx={{
                  p: 2,
                  width: '100%',
                  border: '1px solid',
                  borderColor:
                    selectedSheetId === sheet.uuid ? 'primary.main' : 'divider',
                }}
              >
                <Typography fontWeight={600}>{sheet.period_name}</Typography>
                <Typography variant="body2" color="text.secondary">
                  {getEvaluationSheetStatusLabel(sheet.status)}
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  更新: {formatDateTime(sheet.updated_at)}
                </Typography>
              </Paper>
            </ButtonBase>
          ))}
        </Box>
      )}
    </Paper>
  )
}
