import { Box, Button, Stack } from '@mui/material'
import { useEffect, useMemo, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { getSheet, updateSheet } from '../api'
import { SheetDetailPanel } from '../components/SheetDetailPanel'
import type { ManagerTarget } from '../../evaluation-assignments/types'
import type { ScoreItem, EvaluationSheet } from '../types'
import type { User } from '../../users/types'

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
  const [scoreDraft, setScoreDraft] = useState<Record<string, string>>({})

  const fetchSheetDetail = async (id: string) => {
    setLoading(true)
    onError('')
    try {
      const data = await getSheet(token, id)
      setSheet(data)
      const isSelf = data.employee_uuid === user?.employee_uuid
      const editableScores = isSelf
        ? data.self_evaluation_score
        : data.manager_evaluation_score
      const draft: Record<string, string> = {}
      editableScores.forEach((item) => {
        draft[item.item_uuid] = item.score ? String(item.score) : ''
      })
      setScoreDraft(draft)
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

  const editableScores = sheet
    ? isSelf
      ? sheet.self_evaluation_score
      : sheet.manager_evaluation_score
    : []

  const handleSaveScores = async (isTemporary: boolean) => {
    if (!sheet) return
    setLoading(true)
    onError('')
    onInfo('')
    try {
      const payload = {
        sheet_scores: editableScores.map((item: ScoreItem) => ({
          evaluation_item_id: item.item_uuid,
          score: scoreDraft[item.item_uuid]
            ? Number(scoreDraft[item.item_uuid])
            : null,
        })),
        is_temporary: isTemporary,
      }
      await updateSheet(token, sheet.uuid, payload, isSelf ? 'own' : 'manager')
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
        editableScores={editableScores}
        scoreDraft={scoreDraft}
        canEdit={canEdit}
        loading={loading}
        onSaveTemp={() => handleSaveScores(true)}
        onSaveFinal={() => handleSaveScores(false)}
        onScoreChange={(itemId, value) =>
          setScoreDraft((prev) => ({ ...prev, [itemId]: value }))
        }
      />
    </Stack>
  )
}
