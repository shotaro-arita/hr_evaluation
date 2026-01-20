import { requestJson } from '../../shared/lib/http/client'
import type { ManagerTarget } from './types'

export const listTargets = (token: string) =>
  requestJson<ManagerTarget[]>('/api/evaluations/evaluation_assignments/', {
    headers: { Authorization: `Bearer ${token}` },
  })
