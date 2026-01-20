import { Alert } from '@mui/material'

type Props = {
  error: string
  info: string
}

export const NoticePanel = ({ error, info }: Props) => {
  if (!error && !info) return null
  return (
    <Alert severity={error ? 'error' : 'info'}>{error || info}</Alert>
  )
}
