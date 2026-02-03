import { Box, Button, Stack } from '@mui/material'
import { useEffect, useMemo, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import type { ManagerTarget } from '../../evaluation-assignments/types'
import type { User } from '../../users/types'
import { getSheet, updateSheet } from '../api'
import { SheetDetailPanel } from '../components/SheetDetailPanel'
import type { EvaluationSheet, ScoreItem } from '../types'

type Props = {
  token: string
  user: User | null
  targets: ManagerTarget[]
  loading: boolean
  setLoading: (value: boolean) => void
  onError: (message: string) => void
  onInfo: (message: string) => void
  onRefreshSheets: (employeeId: string) => Promise<void>
}

export const SheetDetailPage = ({
  token,
  user,
  targets,
  loading,
  setLoading,
  onError,
  onInfo,
  onRefreshSheets,
}: Props) => {
  const { sheetId } = useParams()
  const navigate = useNavigate()
  const [sheet, setSheet] = useState<EvaluationSheet | null>(null)
  const [ownDraft, setOwnDraft] = useState<Record<string, string>>({})
  const [managerDraft, setManagerDraft] = useState<Record<string, string>>({})

  const fetchSheetDetail = async (id: string) => {
    setLoading(true)
    onError('')
    try {
      const data = await getSheet(token, id)
      setSheet(data)
      const ownDraftValues: Record<string, string> = {}
      data.self_evaluation_score.forEach((item) => {
        ownDraftValues[item.item_uuid] = item.score ? String(item.score) : ''
      })
      setOwnDraft(ownDraftValues)
      const managerDraftValues: Record<string, string> = {}
      data.manager_evaluation_score.forEach((item) => {
        managerDraftValues[item.item_uuid] = item.score ? String(item.score) : ''
      })
      setManagerDraft(managerDraftValues)
    } catch (err) {
      onError(err instanceof Error ? err.message : 'Unknown error')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    if (!token || !sheetId) return
    void fetchSheetDetail(sheetId)
  }, [token, sheetId, user])

  const isSelf = sheet?.employee_uuid === user?.employee_uuid
  const canEdit = useMemo(() => {
    if (!user || !sheet) return false
    if (isSelf) return true
    return targets.some((target) => target.employee_uuid === sheet.employee_uuid)
  }, [isSelf, sheet, targets, user])

  const ownScores = sheet ? sheet.self_evaluation_score : []
  const managerScores = sheet ? sheet.manager_evaluation_score : []
  const canEditOwn = !!sheet && isSelf
  const canEditManager = !!sheet && !isSelf && canEdit

  const handleSaveOwnScores = async (isTemporary: boolean) => {
    if (!sheet || !canEditOwn) return
    setLoading(true)
    onError('')
    onInfo('')
    try {
      const payload = {
        sheet_scores: ownScores.map((item: ScoreItem) => ({
          evaluation_item_id: item.item_uuid,
          score: ownDraft[item.item_uuid]
            ? Number(ownDraft[item.item_uuid])
            : null,
        })),
        is_temporary: isTemporary,
      }
      await updateSheet(token, sheet.uuid, payload, 'own')
      onInfo(isTemporary ? '下書きを保存しました。' : '評価を保存しました。')
      await fetchSheetDetail(sheet.uuid)
      await onRefreshSheets(sheet.employee_uuid)
    } catch (err) {
      onError(err instanceof Error ? err.message : 'Unknown error')
    } finally {
      setLoading(false)
    }
  }

  const handleSaveManagerScores = async (isTemporary: boolean) => {
    if (!sheet || !canEditManager) return
    setLoading(true)
    onError('')
    onInfo('')
    try {
      const payload = {
        sheet_scores: managerScores.map((item: ScoreItem) => ({
          evaluation_item_id: item.item_uuid,
          score: managerDraft[item.item_uuid]
            ? Number(managerDraft[item.item_uuid])
            : null,
        })),
        is_temporary: isTemporary,
      }
      await updateSheet(token, sheet.uuid, payload, 'manager')
      onInfo(isTemporary ? '下書きを保存しました。' : '評価を保存しました。')
      await fetchSheetDetail(sheet.uuid)
      await onRefreshSheets(sheet.employee_uuid)
    } catch (err) {
      onError(err instanceof Error ? err.message : 'Unknown error')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Stack spacing={2.5}>
      <Box>
        <Button variant="text" onClick={() => navigate('/')}>
          一覧に戻る
        </Button>
      </Box>
      <SheetDetailPanel
        selectedSheet={sheet}
        ownScores={ownScores}
        managerScores={managerScores}
        ownDraft={ownDraft}
        managerDraft={managerDraft}
        canEditOwn={canEditOwn}
        canEditManager={canEditManager}
        loading={loading}
        onSaveOwnTemp={() => handleSaveOwnScores(true)}
        onSaveOwnFinal={() => handleSaveOwnScores(false)}
        onSaveManagerTemp={() => handleSaveManagerScores(true)}
        onSaveManagerFinal={() => handleSaveManagerScores(false)}
        onOwnScoreChange={(itemId, value) =>
          setOwnDraft((prev) => ({ ...prev, [itemId]: value }))
        }
        onManagerScoreChange={(itemId, value) =>
          setManagerDraft((prev) => ({ ...prev, [itemId]: value }))
        }
      />
    </Stack>
  )
}
