import { requestJson } from '../../shared/lib/http/client'
import type { PeriodList } from './types'

export const listPeriods = (token: string) =>
  requestJson<PeriodList>('/api/evaluations/periods/', {
    headers: { Authorization: `Bearer ${token}` },
  })
