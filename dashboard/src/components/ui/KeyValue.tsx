import type { ReactNode } from 'react'
import { cn } from '../../lib/format'

interface KeyValueProps {
  label: string
  value: ReactNode
  /** Tone of the value text. */
  tone?: 'default' | 'active' | 'ok' | 'warn' | 'err' | 'muted'
  /** Larger value for the numbers a presenter needs to read from a distance. */
  size?: 'sm' | 'md' | 'lg'
  className?: string
}

const TONE = {
  default: 'text-fg',
  active: 'text-active',
  ok: 'text-ok',
  warn: 'text-warn',
  err: 'text-err',
  muted: 'text-muted',
}

const SIZE = {
  sm: 'text-[0.78rem]',
  md: 'text-[0.9rem]',
  lg: 'text-[1.1rem] font-medium',
}

/** One telemetry row: muted uppercase label on the left, monospace value on the right. */
export function KeyValue({ label, value, tone = 'default', size = 'sm', className }: KeyValueProps) {
  return (
    <div className={cn('flex items-baseline justify-between gap-3 leading-[1.45rem]', className)}>
      <span className="shrink-0 text-[0.68rem] uppercase tracking-[0.1em] text-muted">{label}</span>
      <span className={cn('num truncate text-right', TONE[tone], SIZE[size])}>{value}</span>
    </div>
  )
}
