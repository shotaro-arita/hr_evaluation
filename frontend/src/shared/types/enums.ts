export const POSITION_LABELS = {
  JR: '一般',
  JS: '一般S',
  AE: '技師補',
  EN: '技師',
  SE: '主任',
  SC: '係長',
} as const

export type Position = keyof typeof POSITION_LABELS

export const JOB_TYPE_LABELS = {
  SD: 'ソフト開発',
  IF: 'インフラ',
  MT: '保守運用',
} as const

export type JobType = keyof typeof JOB_TYPE_LABELS

export const EVALUATION_SHEET_STATUS_LABELS = {
  PENDING: '未完了',
  DRAFT: '下書き',
  COMPLETED: '完了',
  CANCELLED: 'キャンセル',
} as const

export type EvaluationSheetStatus = keyof typeof EVALUATION_SHEET_STATUS_LABELS

export const EVALUATION_ITEM_CATEGORY_LABELS = {
  PERFORMANCE_RESULTS: '成果・業績評価',
  ATTITUDE_SKILLS: '態度・能力評価',
  PROJECT_MANAGEMENT: 'プロジェクト管理技術評価',
  TECHNICAL_SOFTWARE: '技術評価（ソフト開発）',
  TECHNICAL_INFRASTRUCTURE: '技術評価（インフラ構築）',
  TECHNICAL_MAINTENANCE: '技術評価（保守運用）',
} as const

export type EvaluationItemCategory =
  keyof typeof EVALUATION_ITEM_CATEGORY_LABELS

export const getPositionLabel = (value: Position) => POSITION_LABELS[value]
export const getJobTypeLabel = (value: JobType) => JOB_TYPE_LABELS[value]
export const getEvaluationSheetStatusLabel = (value: EvaluationSheetStatus) =>
  EVALUATION_SHEET_STATUS_LABELS[value]
export const getEvaluationItemCategoryLabel = (value: EvaluationItemCategory) =>
  EVALUATION_ITEM_CATEGORY_LABELS[value]
