import { requestJson } from '../../shared/lib/http/client'
import type { LoginRequest, LoginResponse, User } from './types'

export const login = (payload: LoginRequest) =>
  requestJson<LoginResponse>('/api/token/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })

export const getMe = (token: string) =>
  requestJson<User>('/api/evaluations/users/', {
    headers: { Authorization: `Bearer ${token}` },
  })
