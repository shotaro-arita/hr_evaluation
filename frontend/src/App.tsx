import { useState } from 'react'
import './App.css'

function App() {
  const [employeeCode, setEmployeeCode] = useState('')
  const [password, setPassword] = useState('')
  const [employeeId, setEmployeeId] = useState('')
  const [token, setToken] = useState('')
  const [result, setResult] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const requestJson = async <T,>(
    input: RequestInfo | URL,
    init?: RequestInit
  ): Promise<T> => {
    const res = await fetch(input, init)
    const text = await res.text()
    const data = text ? JSON.parse(text) : {}

    if (!res.ok) {
      const message =
        typeof data?.detail === 'string'
          ? data.detail
          : `Request failed: ${res.status}`
      throw new Error(message)
    }

    return data as T
  }

  const handleGetToken = async () => {
    setError('')
    setResult('')
    setLoading(true)
    try {
      const data = await requestJson<{ access: string; refresh: string }>(
        '/api/token/',
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ employee_code: employeeCode, password }),
        }
      )
      setToken(data.access)
      setResult(JSON.stringify(data, null, 2))
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error')
    } finally {
      setLoading(false)
    }
  }

  const handleFetchSheets = async () => {
    setError('')
    setResult('')
    setLoading(true)
    try {
      const data = await requestJson<unknown[]>(
        `/api/evaluations/evaluation_sheets/?employee_id=${encodeURIComponent(
          employeeId
        )}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      )
      setResult(JSON.stringify(data, null, 2))
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header className="header">
        <div>
          <p className="eyebrow">HR Evaluation</p>
          <h1>API 疎通サンプル</h1>
          <p className="subtle">
            /api/token/ でJWTを取得し、/api/evaluations/evaluation_sheets/ を叩く
          </p>
        </div>
      </header>

      <section className="panel">
        <div className="field">
          <label htmlFor="employee-code">employee_code</label>
          <input
            id="employee-code"
            value={employeeCode}
            onChange={(event) => setEmployeeCode(event.target.value)}
            placeholder="employee_code"
            autoComplete="username"
          />
        </div>
        <div className="field">
          <label htmlFor="password">パスワード</label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            placeholder="password"
            autoComplete="current-password"
          />
        </div>
        <button
          className="primary"
          onClick={handleGetToken}
          disabled={loading || !employeeCode || !password}
        >
          トークン取得
        </button>
      </section>

      <section className="panel">
        <div className="field">
          <label htmlFor="employee-id">employee_id</label>
          <input
            id="employee-id"
            value={employeeId}
            onChange={(event) => setEmployeeId(event.target.value)}
            placeholder="UUID"
          />
        </div>
        <button
          className="primary"
          onClick={handleFetchSheets}
          disabled={loading || !token || !employeeId}
        >
          評価シート取得
        </button>
      </section>

      <section className="panel">
        <div className="field">
          <label>アクセストークン</label>
          <textarea value={token} readOnly rows={3} />
        </div>
      </section>

      <section className="panel">
        <label>レスポンス</label>
        {error ? (
          <pre className="output error">{error}</pre>
        ) : (
          <pre className="output">{result || '結果がここに表示されます'}</pre>
        )}
      </section>
    </div>
  )
}

export default App
