import type { ModuleStatus } from '../../state/types'
import { cn } from '../../lib/format'

const COLOR: Record<ModuleStatus, string> = {
  idle: 'bg-queued',
  active: 'bg-active animate-pulse-dot',
  ok: 'bg-ok',
  warn: 'bg-warn',
  error: 'bg-err',
}

interface StatusDotProps {
  status: ModuleStatus
  className?: string
}

/** Small status indicator with the console's colour semantics. */
export function StatusDot({ status, className }: StatusDotProps) {
  return <span className={cn('inline-block size-[0.5rem] shrink-0 rounded-full', COLOR[status], className)} />
}

/** Text colour matching a status, for labels placed next to a dot. */
export function statusText(status: ModuleStatus): string {
  switch (status) {
    case 'active':
      return 'text-active'
    case 'ok':
      return 'text-ok'
    case 'warn':
      return 'text-warn'
    case 'error':
      return 'text-err'
    default:
      return 'text-muted'
  }
}
