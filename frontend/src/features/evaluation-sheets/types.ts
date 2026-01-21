import type {
  EvaluationItemCategory,
  EvaluationSheetStatus,
} from '../../shared/types/enums'

export type ScoreItem = {
  item_uuid: string
  title: string
  category: EvaluationItemCategory
  description: string
  criteria_1: string
  criteria_2: string
  criteria_3: string
  criteria_4: string
  criteria_5: string
  score: number | null
}

export type EvaluationSheet = {
  uuid: string
  period_uuid: string
  period_name: string
  employee_uuid: string
  employee_code: string
  employee_name: string
  self_evaluation_score: ScoreItem[]
  manager_evaluation_score: ScoreItem[]
  own_status: EvaluationSheetStatus
  manager_status: EvaluationSheetStatus
  created_at: string
  updated_at: string
}

export type EvaluationSheetCreateRequest = {
  employee_id: string
  period_id: string
}

export type EvaluationSheetUpdateRequest = {
  sheet_scores: {
    evaluation_item_id: string
    score: number | null
  }[]
  is_temporary: boolean
}
