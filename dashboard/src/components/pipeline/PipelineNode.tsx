import type { PipelineNodeState } from '../../state/types'
import { cn } from '../../lib/format'
import { StatusDot } from '../ui/StatusDot'

interface PipelineNodeProps {
  node: PipelineNodeState
  expanded: boolean
  onToggle(): void
}

/** One module of the autonomy pipeline; click to expand technical details. */
export function PipelineNode({ node, expanded, onToggle }: PipelineNodeProps) {
  return (
    <div className="relative min-w-0 flex-1">
      <button
        type="button"
        onClick={onToggle}
        aria-expanded={expanded}
        className={cn(
          'flex h-full w-full flex-col justify-between border px-2 py-1.5 text-left transition-colors',
          node.status === 'active' && 'border-active/70 bg-active/10',
          node.status === 'warn' && 'border-warn/70 bg-warn/10',
          node.status === 'error' && 'border-err/70 bg-err/10',
          node.status === 'ok' && 'border-line bg-panel-2 hover:border-line-2',
          node.status === 'idle' && 'border-line bg-panel hover:border-line-2',
        )}
      >
        <div className="flex items-center justify-between gap-1">
          <span className="truncate text-[0.6rem] uppercase tracking-[0.14em] text-muted">{node.title}</span>
          <StatusDot status={node.status} />
        </div>
        <div className={cn('truncate text-[0.86rem] font-medium', node.status === 'idle' ? 'text-fg-2' : 'text-fg')}>{node.model}</div>
        <div className="num flex flex-col text-[0.7rem] leading-[1rem] text-fg-2">
          {node.lines.map((line, i) => (
            <span key={i} className={cn('truncate', i === 1 && node.status === 'active' && 'text-active')}>
              {line}
            </span>
          ))}
        </div>
      </button>

      {expanded ? (
        <div className="absolute bottom-full left-0 z-20 mb-1.5 w-[22rem] border border-line-2 bg-panel-2 shadow-[0_12px_30px_rgba(0,0,0,0.6)]">
          <div className="flex items-center justify-between border-b border-line px-2.5 py-1.5">
            <span className="text-[0.66rem] uppercase tracking-[0.14em] text-fg-2">{node.title}</span>
            <span className="text-[0.8rem] font-medium text-fg">{node.model}</span>
          </div>
          <dl className="grid grid-cols-[auto_1fr] gap-x-3 gap-y-0.5 px-2.5 py-2 text-[0.74rem] leading-[1.1rem]">
            {node.details.length ? (
              node.details.map(([k, v]) => (
                <div key={k} className="contents">
                  <dt className="uppercase tracking-[0.08em] text-muted">{k}</dt>
                  <dd className="num text-fg">{v}</dd>
                </div>
              ))
            ) : (
              <dd className="col-span-2 text-muted">No details published.</dd>
            )}
          </dl>
        </div>
      ) : null}
    </div>
  )
}
