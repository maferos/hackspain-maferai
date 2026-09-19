import { useLabState } from '../../state/LabStateProvider'
import { cn, fmtMass, fmtPct, fmtSigned } from '../../lib/format'
import { Panel } from '../ui/Panel'
import { KeyValue } from '../ui/KeyValue'
import { MassChart } from './MassChart'

const MODE_TONE = {
  fast: 'active',
  slow: 'active',
  pulse: 'active',
  stopped: 'muted',
} as const

/** Scientific balance readout: hero number, target, dosing state and history. */
export function BalancePanel() {
  const { state } = useLabState()
  const b = state.balance
  const ingredient = b.ingredientId ? state.recipe.ingredients.find((i) => i.id === b.ingredientId) ?? null : null
  const remaining = b.targetMass - b.netMass
  const progress = b.targetMass > 0 ? Math.min(1, Math.max(0, b.netMass / b.targetMass)) : 0
  const batchProgress = b.batchTargetMass > 0 ? Math.min(1, b.totalMass / b.batchTargetMass) : 0
  const dosing = b.mode !== 'stopped'
  const right = (
    <span className={cn('num text-[0.72rem] tracking-[0.12em]', ingredient ? 'text-fg-2' : 'text-muted')}>
      {b.id ? `${b.id.toUpperCase()} · ` : ''}
      {ingredient ? ingredient.compound.toUpperCase() : 'NO INGREDIENT'}
    </span>
  )

  return (
    <Panel title="Analytical balance" right={right} bodyClassName="flex flex-col px-2.5 py-2">
      <div className="flex items-end justify-between">
        <div className="flex items-baseline gap-1.5">
          <span className="num text-[3.4rem] font-medium leading-none tracking-tight text-fg">{fmtMass(b.netMass)}</span>
          <span className="text-[1.1rem] text-fg-2">g</span>
        </div>
        <div className="flex flex-col items-end gap-1 pb-1">
          <span className="text-[0.62rem] uppercase tracking-[0.14em] text-muted">Net since tare</span>
          <span className={cn('num flex items-center gap-1.5 text-[0.72rem] tracking-[0.14em]', b.stable ? 'text-ok' : 'text-warn')}>
            <span className={cn('size-2 rounded-full', b.stable ? 'bg-ok' : 'bg-warn animate-pulse-dot')} />
            {b.stable ? 'STABLE' : 'SETTLING'}
          </span>
        </div>
      </div>

      <div className="mt-2 border-t border-line pt-1">
        <KeyValue label="Target" value={`${fmtMass(b.targetMass)} g`} size="md" />
        <KeyValue label="Remaining" value={`${fmtSigned(-remaining)} g`} tone={Math.abs(remaining) <= 0.01 ? 'ok' : 'default'} size="md" />
        <div className="flex items-center gap-2 py-1">
          <span className="block h-1.5 flex-1 overflow-hidden bg-line">
            <span className="block h-full bg-active transition-[width] duration-200" style={{ width: fmtPct(progress) }} />
          </span>
          <span className="num w-12 text-right text-[0.8rem] text-fg">{fmtPct(progress, 1)}</span>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-x-4 border-t border-line pt-1">
        <KeyValue label="Mode" value={b.mode.toUpperCase()} tone={MODE_TONE[b.mode]} />
        <KeyValue label="Flow" value={`${b.flowRate.toFixed(3)} g/s`} tone={dosing ? 'default' : 'muted'} />
        <KeyValue label="Stable" value={b.stable ? 'YES' : 'NO'} tone={b.stable ? 'ok' : 'warn'} />
        <KeyValue label="Ingredient" value={ingredient?.compound ?? '—'} tone={ingredient ? 'default' : 'muted'} />
      </div>

      <div className="mt-1 border-t border-line pt-1.5">
        <div className="flex items-baseline justify-between text-[0.62rem] uppercase tracking-[0.14em] text-muted">
          <span>Batch total</span>
          <span className="num text-[0.78rem] normal-case tracking-normal text-fg">
            {fmtMass(b.totalMass)} / {fmtMass(b.batchTargetMass)} g
          </span>
        </div>
        <span className="mt-1 block h-1 overflow-hidden bg-line">
          <span className="block h-full bg-ok/80 transition-[width] duration-200" style={{ width: fmtPct(batchProgress) }} />
        </span>
      </div>

      <div className="mt-2 flex min-h-[6rem] flex-1 flex-col border-t border-line pt-1.5">
        <div className="flex items-baseline justify-between text-[0.62rem] uppercase tracking-[0.14em] text-muted">
          <span>Net mass vs target</span>
          <span>{b.historyWindow} s window</span>
        </div>
        <div className="min-h-0 flex-1">
          <MassChart history={b.history} target={b.targetMass} window={b.historyWindow} now={state.run.elapsedSeconds} />
        </div>
      </div>
    </Panel>
  )
}
