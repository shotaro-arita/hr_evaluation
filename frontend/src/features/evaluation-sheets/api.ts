import { requestJson } from '../../shared/lib/http/client'
import type {
  EvaluationSheet,
  EvaluationSheetCreateRequest,
  EvaluationSheetUpdateRequest,
} from './types'

export const listSheets = (token: string, employeeId: string) =>
  requestJson<EvaluationSheet[]>(
    `/api/evaluations/evaluation_sheets/?employee_id=${encodeURIComponent(
      employeeId
    )}`,
    {
      headers: { Authorization: `Bearer ${token}` },
    }
  )

export const getSheet = (token: string, sheetId: string) =>
  requestJson<EvaluationSheet>(
    `/api/evaluations/evaluation_sheets/${sheetId}/`,
    {
      headers: { Authorization: `Bearer ${token}` },
    }
  )

export const createSheet = (token: string, payload: EvaluationSheetCreateRequest) =>
  requestJson<EvaluationSheet>('/api/evaluations/evaluation_sheets/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(payload),
  })

export const updateSheet = (
  token: string,
  sheetId: string,
  payload: EvaluationSheetUpdateRequest,
  mode: 'own' | 'manager'
) => {
  const action = mode === 'own' ? 'update_own' : 'update_by_manager'
  return requestJson<EvaluationSheet>(
    `/api/evaluations/evaluation_sheets/${sheetId}/${action}/`,
    {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(payload),
    }
  )
}
