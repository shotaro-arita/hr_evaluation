import { Box, Container, CssBaseline, Stack } from '@mui/material'
import { ThemeProvider, createTheme } from '@mui/material/styles'
import { useEffect, useMemo, useState } from 'react'
import { Route, Routes, useNavigate } from 'react-router-dom'
import { HeroHeader } from './app/components/HeroHeader'
import { NoticePanel } from './app/components/NoticePanel'
import { listTargets } from './features/evaluation-assignments/api'
import { TargetSelectorPanel } from './features/evaluation-assignments/components/TargetSelectorPanel'
import type { ManagerTarget } from './features/evaluation-assignments/types'
import { createSheet, listSheets } from './features/evaluation-sheets/api'
import { SheetListPanel } from './features/evaluation-sheets/components/SheetListPanel'
import { SheetDetailPage } from './features/evaluation-sheets/pages/SheetDetailPage'
import type { EvaluationSheet } from './features/evaluation-sheets/types'
import { listPeriods } from './features/periods/api'
import { LoginPanel } from './features/users/components/LoginPanel'
import { UserOverviewPanel } from './features/users/components/UserOverviewPanel'
import { useAuth } from './features/users/hooks/useAuth'
import type { User } from './features/users/types'

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#0ea5e9',
    },
    secondary: {
      main: '#0f766e',
    },
    background: {
      default: '#f1f5f9',
      paper: '#ffffff',
    },
    text: {
      primary: '#0f172a',
      secondary: '#475569',
    },
  },
  typography: {
    fontFamily: '"IBM Plex Sans","Space Grotesk","Segoe UI",sans-serif',
    h1: {
      fontSize: '2.2rem',
      fontWeight: 700,
    },
    h2: {
      fontSize: '1.25rem',
      fontWeight: 700,
    },
  },
  shape: {
    borderRadius: 16,
  },
})

function App() {
  const [employeeCode, setEmployeeCode] = useState('')
  const [password, setPassword] = useState('')
  const [currentPeriodId, setCurrentPeriodId] = useState<string | null>(null)
  const [targets, setTargets] = useState<ManagerTarget[]>([])
  const [selectedEmployeeId, setSelectedEmployeeId] = useState('')
  const [sheets, setSheets] = useState<EvaluationSheet[]>([])
  const [selectedSheetId, setSelectedSheetId] = useState<string | null>(null)
  const [targetStatuses, setTargetStatuses] = useState<
    Record<
      string,
      Pick<EvaluationSheet, 'own_status' | 'manager_status'> | null
    >
  >({})
  const [targetStatusLoading, setTargetStatusLoading] = useState(false)
  const [error, setError] = useState('')
  const [info, setInfo] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const {
    token,
    user,
    loading: authLoading,
    error: authError,
    loginWithPassword,
    logout,
  } = useAuth()

  const resetDashboard = () => {
    setTargets([])
    setCurrentPeriodId(null)
    setSelectedEmployeeId('')
    setSheets([])
    setSelectedSheetId(null)
  }

  const bootstrap = async (activeUser: User) => {
    setLoading(true)
    setError('')
    try {
      const periodData = await listPeriods(token)
      setCurrentPeriodId(periodData.current_period_uuid)
      if (activeUser.is_manager) {
        const managerTargets = await listTargets(token)
        setTargets(managerTargets)
      } else {
        setTargets([])
      }
      setSelectedEmployeeId(activeUser.employee_uuid)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error')
    } finally {
      setLoading(false)
    }
  }

  const fetchSheets = async (employeeId: string) => {
    if (!employeeId) return
    setLoading(true)
    setError('')
    try {
      const data = await listSheets(token, employeeId)
      setSheets(data)
      setSelectedSheetId(null)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error')
    } finally {
      setLoading(false)
    }
  }

  const fetchTargetStatuses = async (employeeIds: string[]) => {
    if (!currentPeriodId || employeeIds.length === 0) return
    setTargetStatusLoading(true)
    try {
      const uniqueIds = Array.from(new Set(employeeIds))
      const entries = await Promise.all(
        uniqueIds.map(async (employeeId) => {
          const list = await listSheets(token, employeeId)
          const current = list.find(
            (sheet) => sheet.period_uuid === currentPeriodId
          )
          return [
            employeeId,
            current
              ? {
                  own_status: current.own_status,
                  manager_status: current.manager_status,
                }
              : null,
          ] as const
        })
      )
      setTargetStatuses(Object.fromEntries(entries))
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error')
    } finally {
      setTargetStatusLoading(false)
    }
  }

  const handleCreateSheet = async () => {
    if (!currentPeriodId || !selectedEmployeeId) {
      setError('今期または対象者が選択されていません。')
      return
    }
    setLoading(true)
    setError('')
    setInfo('')
    try {
      await createSheet(token, {
        employee_id: selectedEmployeeId,
        period_id: currentPeriodId,
      })
      setInfo('今期の評価シートを作成しました。')
      await fetchSheets(selectedEmployeeId)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    if (user && token) {
      void bootstrap(user)
    } else {
      resetDashboard()
    }
  }, [user, token])

  useEffect(() => {
    if (token && selectedEmployeeId) {
      void fetchSheets(selectedEmployeeId)
    }
  }, [token, selectedEmployeeId])

  useEffect(() => {
    if (!token || !user?.is_manager || !currentPeriodId) return
    const targetIds = [user.employee_uuid, ...targets.map((t) => t.employee_uuid)]
    void fetchTargetStatuses(targetIds)
  }, [token, user, targets, currentPeriodId])

  const targetOptions = useMemo(() => {
    const options = targets.map((target) => ({
      employeeId: target.employee_uuid,
      label: `${target.employee_code} ${target.name}`,
      status: targetStatuses[target.employee_uuid] ?? null,
    }))
    if (user) {
      options.unshift({
        employeeId: user.employee_uuid,
        label: `${user.employee_code} ${user.name}`,
        status: targetStatuses[user.employee_uuid] ?? null,
        isSelf: true,
      })
    }
    return options
  }, [targetStatuses, targets, user])

  const canCreateSheet = useMemo(
    () => !loading && !!currentPeriodId && !!selectedEmployeeId,
    [currentPeriodId, loading, selectedEmployeeId]
  )

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="lg" sx={{ py: 6 }}>
        <Stack spacing={4}>
          <HeroHeader user={user} token={token} />

          {!token ? (
            <LoginPanel
              employeeCode={employeeCode}
              password={password}
              loading={loading || authLoading}
              onEmployeeCodeChange={setEmployeeCode}
              onPasswordChange={setPassword}
              onSubmit={() => loginWithPassword(employeeCode, password)}
            />
          ) : (
            <Routes>
              <Route
                path="/"
                element={
                  <Box
                    sx={{
                      display: 'grid',
                      gap: 2.5,
                      gridTemplateColumns: { xs: '1fr', md: 'repeat(2, 1fr)' },
                    }}
                  >
                    <Box sx={{ gridColumn: { xs: 'auto', md: '1 / -1' } }}>
                      <UserOverviewPanel user={user} onLogout={logout} />
                    </Box>
                    {user?.is_manager ? (
                      <Box sx={{ gridColumn: { xs: 'auto', md: '1 / -1' } }}>
                        <TargetSelectorPanel
                          targets={targetOptions}
                          selectedEmployeeId={selectedEmployeeId}
                          helperText={
                            targets.length === 0
                              ? '管理者対象が登録されていません。'
                              : `${targets.length}名の評価対象がいます。`
                          }
                          loading={targetStatusLoading}
                          onChange={setSelectedEmployeeId}
                        />
                      </Box>
                    ) : null}
                    <Box sx={{ gridColumn: { xs: 'auto', md: '1 / -1' } }}>
                      <SheetListPanel
                        sheets={sheets}
                        selectedSheetId={selectedSheetId}
                        loading={loading}
                        onReload={() => fetchSheets(selectedEmployeeId)}
                        onCreate={handleCreateSheet}
                        canCreate={canCreateSheet}
                        onSelect={(sheetId) => {
                          setSelectedSheetId(sheetId)
                          navigate(`/sheets/${sheetId}`)
                        }}
                        selectedEmployeeId={selectedEmployeeId}
                      />
                    </Box>
                  </Box>
                }
              />
              <Route
                path="/sheets/:sheetId"
                element={
                  <SheetDetailPage
                    token={token}
                    user={user}
                    targets={targets}
                    loading={loading}
                    setLoading={setLoading}
                    onError={setError}
                    onInfo={setInfo}
                    onRefreshSheets={fetchSheets}
                  />
                }
              />
            </Routes>
          )}

          <NoticePanel error={error || authError} info={info} />
        </Stack>
      </Container>
    </ThemeProvider>
  )
}

export default App
