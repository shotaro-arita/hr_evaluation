import {
  FormControl,
  FormHelperText,
  InputLabel,
  MenuItem,
  Paper,
  Select,
  Typography,
} from '@mui/material'

type Option = {
  value: string
  label: string
}

type Props = {
  options: Option[]
  selectedEmployeeId: string
  helperText: string
  onChange: (value: string) => void
}

export const TargetSelectorPanel = ({
  options,
  selectedEmployeeId,
  helperText,
  onChange,
}: Props) => {
  return (
    <Paper
      elevation={0}
      sx={{ p: 3, border: '1px solid', borderColor: 'divider' }}
    >
      <Typography variant="h2">評価対象</Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
        一覧を確認したい対象者を選択します。
      </Typography>
      <FormControl fullWidth sx={{ mt: 2 }}>
        <InputLabel id="target-select-label">評価対象</InputLabel>
        <Select
          labelId="target-select-label"
          value={selectedEmployeeId}
          label="評価対象"
          onChange={(event) => onChange(event.target.value)}
        >
          {options.map((option) => (
            <MenuItem key={option.value} value={option.value}>
              {option.label}
            </MenuItem>
          ))}
        </Select>
        <FormHelperText>{helperText}</FormHelperText>
      </FormControl>
    </Paper>
  )
}
