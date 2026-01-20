import { API_BASE_URL } from '../config'
import { ApiError } from './errors'

const withBaseUrl = (input: RequestInfo | URL) => {
  if (typeof input === 'string' && input.startsWith('/')) {
    return `${API_BASE_URL}${input}`
  }
  return input
}

export const requestJson = async <T,>(
  input: RequestInfo | URL,
  init?: RequestInit
): Promise<T> => {
  const response = await fetch(withBaseUrl(input), init)
  const text = await response.text()
  const data = text ? JSON.parse(text) : null

  if (!response.ok) {
    if (response.status === 401 && typeof window !== 'undefined') {
      window.dispatchEvent(new CustomEvent('auth:logout'))
    }
    throw new ApiError(response.status, data?.detail ?? data)
  }

  return data as T
}
