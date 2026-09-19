import { Pause, Play, RotateCcw } from 'lucide-react'
import type { MacroPhase, ModuleStatus } from '../state/types'
import { useLabState } from '../state/LabStateProvider'
import { cn, fmtClock, fmtPct } from '../lib/format'
import { StatusDot } from './ui/StatusDot'

const PHASES: Array<[MacroPhase, string]> = [
  ['perceive', 'PERCEIVE'],
  ['identify', 'IDENTIFY'],
  ['plan', 'PLAN'],
  ['move', 'MOVE'],
  ['dose', 'DOSE'],
  ['verify', 'VERIFY'],
]

const SPEEDS = [1, 2, 4]

function Sep() {
  return <span className="text-line-2">|</span>
}

/** Thin top bar: identity, macro phase, run identifiers, progress and source. */
export function HeaderStatus() {
  const { state, source, connection, liveUrl, demo, setSource } = useLabState()
  const { run, recipe } = state

  const runDot: ModuleStatus = run.status === 'running' ? 'active' : run.status === 'completed' ? 'ok' : run.status === 'failed' ? 'error' : 'idle'
  const pill =
    run.status === 'running'
      ? 'border-active/60 text-active'
      : run.status === 'completed'
        ? 'border-ok/60 text-ok'
        : run.status === 'failed'
          ? 'border-err/60 text-err'
          : 'border-line-2 text-muted'
  const connDot: ModuleStatus = connection === 'open' ? 'ok' : connection === 'connecting' ? 'active' : connection === 'error' ? 'error' : 'idle'

  return (
    <header className="flex h-10 shrink-0 items-center gap-3 border border-line bg-panel px-3">
      <div className="flex items-baseline gap-2.5">
        <span className="text-[0.95rem] font-bold tracking-[0.22em] text-fg">MAFERAI</span>
        <span className="text-[0.7rem] uppercase tracking-[0.14em] text-fg-2">Autonomous Formulation Lab</span>
      </div>

      <div className="h-5 w-px bg-line-2" />

      <ol className="flex items-center gap-0.5" aria-label="Autonomy phase">
        {PHASES.map(([id, label], i) => (
          <li key={id} className="flex items-center gap-0.5">
            <span
              className={cn(
                'px-1.5 py-0.5 text-[0.66rem] font-semibold tracking-[0.16em] transition-colors',
                run.phase === id ? 'bg-active/15 text-active' : 'text-muted',
              )}
            >
              {label}
            </span>
            {i < PHASES.length - 1 ? <span className="text-[0.6rem] text-muted/70">{'→'}</span> : null}
          </li>
        ))}
      </ol>

      <div className="flex-1" />

      <div className="num flex items-center gap-3 text-[0.8rem] text-fg">
        <span className="flex items-center gap-1.5">
          <StatusDot status={runDot} />
          <span className="tracking-[0.12em]">{run.mode.toUpperCase()}</span>
        </span>
        <Sep />
        <span>{run.id}</span>
        <Sep />
        <span>{recipe.id}</span>
        <Sep />
        <span>
          {fmtClock(run.elapsedSeconds)} <span className="text-muted">elapsed</span>
        </span>
        <Sep />
        <span className="flex items-center gap-2">
          <span className="block h-1.5 w-24 overflow-hidden bg-line">
            <span className="block h-full bg-active transition-[width] duration-300" style={{ width: fmtPct(run.progress) }} />
          </span>
          <span className="w-9 text-right">{fmtPct(run.progress)}</span>
        </span>
        <Sep />
        <span className={cn('border px-2 py-0.5 text-[0.68rem] font-semibold tracking-[0.16em]', pill)}>
          {run.status === 'completed' ? 'COMPLETE' : run.status.toUpperCase()}
        </span>
      </div>

      <div className="h-5 w-px bg-line-2" />

      <div className="flex items-center gap-1.5">
        <div className="flex border border-line-2 text-[0.66rem] font-semibold tracking-[0.14em]">
          <button
            type="button"
            onClick={() => setSource('demo')}
            className={cn('px-2 py-0.5', source === 'demo' ? 'bg-panel-3 text-fg' : 'text-muted hover:text-fg-2')}
          >
            DEMO
          </button>
          <button
            type="button"
            onClick={() => setSource('live')}
            title={liveUrl}
            className={cn('flex items-center gap-1.5 px-2 py-0.5', source === 'live' ? 'bg-panel-3 text-fg' : 'text-muted hover:text-fg-2')}
          >
            {source === 'live' ? <StatusDot status={connDot} /> : null}
            LIVE
          </button>
        </div>

        {demo ? (
          <div className="flex items-center gap-0.5 border border-line-2">
            <button
              type="button"
              onClick={() => (demo.playing ? demo.pause() : demo.play())}
              className="p-1 text-fg-2 hover:text-fg"
              title={demo.playing ? 'Pause demo' : 'Play demo'}
            >
              {demo.playing ? <Pause size={13} /> : <Play size={13} />}
            </button>
            <button type="button" onClick={() => demo.restart()} className="p-1 text-fg-2 hover:text-fg" title="Restart demo">
              <RotateCcw size={13} />
            </button>
            <button
              type="button"
              onClick={() => demo.setSpeed(SPEEDS[(SPEEDS.indexOf(demo.speed) + 1) % SPEEDS.length] ?? 1)}
              className="num w-8 py-0.5 text-[0.7rem] text-fg-2 hover:text-fg"
              title="Playback speed"
            >
              {demo.speed}
              {'×'}
            </button>
          </div>
        ) : null}
      </div>
    </header>
  )
}
