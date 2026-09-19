import type { EventLevel } from '../state/types'
import { useLabState } from '../state/LabStateProvider'
import { cn, fmtStamp } from '../lib/format'
import { Panel } from './ui/Panel'

const VISIBLE = 7

const LEVEL_DOT: Record<EventLevel, string> = {
  info: 'bg-fg-2/60',
  ok: 'bg-ok',
  warn: 'bg-warn',
  error: 'bg-err',
}

const LEVEL_TEXT: Record<EventLevel, string> = {
  info: 'text-fg-2',
  ok: 'text-fg',
  warn: 'text-warn',
  error: 'text-err',
}

/** Latest autonomy events, newest at the bottom. Recovery shows up here. */
export function EventLog() {
  const { state } = useLabState()
  const events = state.events.slice(-VISIBLE)
  const right = <span className="num text-[0.7rem] tracking-[0.1em] text-muted">last {VISIBLE}</span>
  return (
    <Panel title="Events" right={right} bodyClassName="flex flex-col justify-end px-2.5 py-1.5">
      <ol className="num flex flex-col text-[0.76rem] leading-[1.42rem]">
        {events.map((ev) => (
          <li key={ev.id} className="flex min-w-0 items-center gap-2">
            <span className="shrink-0 text-muted">{fmtStamp(ev.time)}</span>
            <span className={cn('size-1.5 shrink-0 rounded-full', LEVEL_DOT[ev.level])} />
            <span className={cn('min-w-0 flex-1 truncate', LEVEL_TEXT[ev.level])}>{ev.message}</span>
          </li>
        ))}
        {events.length === 0 ? <li className="text-muted">no events yet</li> : null}
      </ol>
    </Panel>
  )
}
