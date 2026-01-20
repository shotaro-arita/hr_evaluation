import { useCallback, useEffect, useState } from 'react'

import { login, getMe } from '../api'
import type { User } from '../types'
import { clearToken, getToken, setToken } from '../../../shared/lib/http/auth'
import { ApiError } from '../../../shared/lib/http/errors'

export const useAuth = () => {
  const [token, setTokenState] = useState(() => getToken())
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const loadUser = useCallback(
    async (accessToken: string) => {
      if (!accessToken) return
      setLoading(true)
      setError('')
      try {
        const me = await getMe(accessToken)
        setUser(me)
      } catch (err) {
        if (err instanceof ApiError && err.status === 401) {
          clearToken()
          setTokenState('')
          setUser(null)
          setError('セッションが切れました。再度ログインしてください。')
          return
        }
        setError(err instanceof Error ? err.message : 'Unknown error')
      } finally {
        setLoading(false)
      }
    },
    [setUser]
  )

  const loginWithPassword = async (employee_code: string, password: string) => {
    setLoading(true)
    setError('')
    try {
      const data = await login({ employee_code, password })
      setToken(data.access)
      setTokenState(data.access)
      await loadUser(data.access)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error')
    } finally {
      setLoading(false)
    }
  }

  const logout = () => {
    clearToken()
    setTokenState('')
    setUser(null)
  }

  useEffect(() => {
    if (token) {
      void loadUser(token)
    }
  }, [token, loadUser])

  return {
    token,
    user,
    loading,
    error,
    loginWithPassword,
    logout,
    refreshUser: () => (token ? loadUser(token) : Promise.resolve()),
    setError,
  }
}
