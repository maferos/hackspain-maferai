import type { ReactNode } from 'react'
import { cn } from '../../lib/format'

interface PanelProps {
  title: string
  /** Content aligned to the right of the title bar. */
  right?: ReactNode
  children: ReactNode
  className?: string
  bodyClassName?: string
}

/** Panel chrome shared by every section: thin border, small uppercase title. */
export function Panel({ title, right, children, className, bodyClassName }: PanelProps) {
  return (
    <section className={cn('flex h-full min-h-0 min-w-0 flex-col overflow-hidden border border-line bg-panel', className)}>
      <header className="flex h-7 shrink-0 items-center justify-between gap-2 border-b border-line px-2.5">
        <h2 className="truncate text-[0.72rem] font-semibold uppercase tracking-[0.14em] text-fg-2">{title}</h2>
        {right ? <div className="flex shrink-0 items-center gap-2">{right}</div> : null}
      </header>
      <div className={cn('relative min-h-0 min-w-0 flex-1', bodyClassName)}>{children}</div>
    </section>
  )
}
