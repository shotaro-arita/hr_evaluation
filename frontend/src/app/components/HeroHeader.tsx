import { Box, Chip, Paper, Stack, Typography } from '@mui/material'
import type { User } from '../../features/users/types'

type Props = {
  user: User | null
  token: string
}

export const HeroHeader = ({ user, token }: Props) => {
  return (
    <Paper
      elevation={0}
      sx={{
        p: 3,
        border: '1px solid',
        borderColor: 'divider',
        background:
          'linear-gradient(120deg, rgba(224,242,254,0.95), rgba(248,250,252,0.95))',
      }}
    >
      <Stack
        direction={{ xs: 'column', md: 'row' }}
        spacing={3}
        alignItems={{ xs: 'flex-start', md: 'center' }}
        justifyContent="space-between"
      >
        <Box>
          <Typography
            variant="overline"
            sx={{ letterSpacing: '0.3em', color: 'text.secondary' }}
          >
            HR Evaluation
          </Typography>
          <Typography variant="h1" sx={{ mt: 1 }}>
            評価シート
          </Typography>
          <Typography sx={{ mt: 1, color: 'text.secondary' }}>
            ログインから一覧・編集までを一画面で確認できる社内ツールのプロトタイプ。
          </Typography>
        </Box>
        <Paper
          elevation={0}
          sx={{
            p: 2.5,
            minWidth: { xs: '100%', md: 260 },
            border: '1px solid',
            borderColor: 'divider',
            backgroundColor: 'rgba(255,255,255,0.9)',
          }}
        >
          <Typography
            variant="overline"
            sx={{ letterSpacing: '0.25em', color: 'text.secondary' }}
          >
            ステータス
          </Typography>
          <Typography variant="h6" sx={{ mt: 1 }}>
            {token ? 'ログイン中' : '未ログイン'}
          </Typography>
          <Typography sx={{ color: 'text.secondary', mt: 1 }}>
            {user ? `${user.employee_code} ${user.name}` : 'まずログインしてください'}
          </Typography>
          {user?.is_manager && (
            <Stack direction="row" spacing={1} sx={{ mt: 2 }}>
              <Chip label="管理者" color="primary" size="small" />
              <Chip
                label={`対象 ${user.manager_target_count} 名`}
                size="small"
                variant="outlined"
              />
            </Stack>
          )}
        </Paper>
      </Stack>
    </Paper>
  )
}
