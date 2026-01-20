const TOKEN_KEY = 'hr_eval_access_token'

export const getToken = (): string => localStorage.getItem(TOKEN_KEY) ?? ''

export const setToken = (token: string) => {
  localStorage.setItem(TOKEN_KEY, token)
}

export const clearToken = () => {
  localStorage.removeItem(TOKEN_KEY)
}
