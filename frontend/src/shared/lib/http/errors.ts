export class ApiError extends Error {
  status: number
  detail: unknown

  constructor(status: number, detail: unknown) {
    super(typeof detail === 'string' ? detail : `Request failed: ${status}`)
    this.status = status
    this.detail = detail
  }
}
