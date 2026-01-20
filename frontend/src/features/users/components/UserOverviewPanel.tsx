import { Box, Button, Paper, Stack, Typography } from '@mui/material'
import { getJobTypeLabel, getPositionLabel } from '../../../shared/types/enums'
import type { User } from '../types'

type Props = {
  user: User | null
  onLogout: () => void
}

export const UserOverviewPanel = ({ user, onLogout }: Props) => {
  return (
    <Paper
      elevation={0}
      sx={{ p: 3, border: '1px solid', borderColor: 'divider' }}
    >
      <Stack spacing={1}>
        <Typography variant="h2">ユーザー情報</Typography>
        <Typography variant="body2" color="text.secondary">
          評価対象の選択や権限確認に使います。
        </Typography>
      </Stack>
      {user ? (
        <Box
          sx={{
            mt: 2,
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))',
            gap: 2,
            alignItems: 'center',
          }}
        >
          <Box>
            <Typography variant="overline" color="text.secondary">
              氏名
            </Typography>
            <Typography fontWeight={600}>{user.name}</Typography>
          </Box>
          <Box>
            <Typography variant="overline" color="text.secondary">
              社員ID
            </Typography>
            <Typography fontWeight={600}>{user.employee_code}</Typography>
          </Box>
          <Box>
            <Typography variant="overline" color="text.secondary">
              ポジション
            </Typography>
            <Typography fontWeight={600}>
              {getPositionLabel(user.position)}
            </Typography>
          </Box>
          <Box>
            <Typography variant="overline" color="text.secondary">
              職種
            </Typography>
            <Typography fontWeight={600}>
              {getJobTypeLabel(user.job_type)}
            </Typography>
          </Box>
          {user.manager_target_count > 0 && (
            <Box>
              <Typography variant="overline" color="text.secondary">
                評価対象数
              </Typography>
              <Typography fontWeight={600}>{user.manager_target_count}</Typography>
            </Box>
          )}
          <Box>
            <Button variant="outlined" onClick={onLogout}>
              ログアウト
            </Button>
          </Box>
        </Box>
      ) : (
        <Typography sx={{ mt: 2 }} color="text.secondary">
          読み込み中...
        </Typography>
      )}
    </Paper>
  )
}
