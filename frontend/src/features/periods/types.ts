export type Period = {
  uuid: string
  name: string
  start_date: string
  end_date: string
  is_current: boolean
}

export type PeriodList = {
  periods: Period[]
  current_period_uuid: string | null
}
