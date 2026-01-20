import type { JobType, Position } from '../../shared/types/enums'

export type LoginRequest = {
  employee_code: string
  password: string
}

export type LoginResponse = {
  access: string
  refresh: string
}

export type User = {
  user_uuid: string
  employee_uuid: string
  employee_code: string
  name: string
  position: Position
  job_type: JobType
  is_manager: boolean
  manager_target_count: number
}
