import type { JobType, Position } from '../../shared/types/enums'

export type ManagerTarget = {
  employee_uuid: string
  employee_code: string
  name: string
  position: Position
  job_type: JobType
  role: string
}
