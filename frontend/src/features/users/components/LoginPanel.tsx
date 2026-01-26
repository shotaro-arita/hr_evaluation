import { Button, Paper, Stack, TextField, Typography } from '@mui/material'
import type { FormEvent } from 'react'

type Props = {
  employeeCode: string
  password: string
  loading: boolean
  onEmployeeCodeChange: (value: string) => void
  onPasswordChange: (value: string) => void
  onSubmit: () => void
}

export const LoginPanel = ({
  employeeCode,
  password,
  loading,
  onEmployeeCodeChange,
  onPasswordChange,
  onSubmit,
}: Props) => {
  const handleSubmit = (event: FormEvent) => {
    event.preventDefault()
    onSubmit()
  }

  return (
    <Paper
      elevation={0}
      sx={{ p: 3, maxWidth: 520, border: '1px solid', borderColor: 'divider' }}
    >
      <Typography variant="h2">ログイン</Typography>
      <Stack component="form" spacing={2} sx={{ mt: 2 }} onSubmit={handleSubmit}>
        <TextField
          label="社員ID"
          value={employeeCode}
          onChange={(event) => onEmployeeCodeChange(event.target.value)}
          placeholder="employee_code"
          autoComplete="username"
          size="small"
          fullWidth
        />
        <TextField
          label="パスワード"
          type="password"
          value={password}
          onChange={(event) => onPasswordChange(event.target.value)}
          placeholder="password"
          autoComplete="current-password"
          size="small"
          fullWidth
        />
        <Button
          variant="contained"
          type="submit"
          disabled={loading || !employeeCode || !password}
        >
          ログインする
        </Button>
      </Stack>
    </Paper>
  )
}
