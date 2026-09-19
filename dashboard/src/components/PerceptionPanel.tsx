import type { ModuleStatus } from '../state/types'
import { useLabState } from '../state/LabStateProvider'
import { cn, fmtMetres } from '../lib/format'
import { Panel } from './ui/Panel'
import { KeyValue } from './ui/KeyValue'
import { StatusDot, statusText } from './ui/StatusDot'

const MODULES: Array<[keyof ReturnType<typeof modulesOf>, string]> = [
  ['detector', 'Detector'],
  ['localizer', 'Localizer'],
  ['barcode', 'Barcode'],
  ['wristCam', 'Wrist cam'],
]

function modulesOf(m: { detector: ModuleStatus; localizer: ModuleStatus; barcode: ModuleStatus; wristCam: ModuleStatus }) {
  return m
}

/** What the robot perceives. Never simulator ground truth. */
export function PerceptionPanel() {
  const { state } = useLabState()
  const p = state.perception
  const pos = p.estimatedPosition
  const right = <span className="num text-[0.7rem] tracking-[0.12em] text-fg-2">CAM {p.activeCamera.toUpperCase()}</span>

  return (
    <Panel title="Perception" right={right} bodyClassName="flex flex-col px-2.5 py-1.5">
      <div className="grid grid-cols-4 gap-1 border-b border-line pb-1.5">
        {MODULES.map(([key, label]) => (
          <div key={key} className="flex min-w-0 items-center gap-1.5">
            <StatusDot status={p.modules[key]} />
            <span className={cn('truncate text-[0.62rem] uppercase tracking-[0.1em]', statusText(p.modules[key]))}>{label}</span>
          </div>
        ))}
      </div>
      <div className="grid flex-1 grid-cols-[1.1fr_1fr] gap-x-4 pt-1">
        <div>
          <KeyValue label="Vessels" value={String(p.detections)} size="md" />
          <KeyValue label="Target" value={p.target ?? '—'} tone={p.target ? 'active' : 'muted'} size="md" />
          <KeyValue label="Class" value={p.targetClass ?? '—'} tone={p.targetClass ? 'default' : 'muted'} />
          <KeyValue label="Confidence" value={p.confidence !== null ? p.confidence.toFixed(2) : '—'} tone={p.confidence !== null ? 'default' : 'muted'} />
          <KeyValue label="Barcode" value={p.barcode ?? '—'} tone={p.barcodeStatus === 'verified' ? 'ok' : p.barcode ? 'active' : 'muted'} />
        </div>
        <div>
          <KeyValue label="Identity" value={p.identity ?? '—'} tone={p.identity ? 'ok' : 'muted'} size="md" />
          <KeyValue label="Container" value={p.containerMl !== null ? `${p.containerMl} mL` : '—'} tone={p.containerMl !== null ? 'default' : 'muted'} />
          <div className="mt-0.5 flex items-baseline justify-between whitespace-nowrap text-[0.62rem] uppercase tracking-[0.12em] text-muted">
            <span>Position (est.)</span>
            <span className="num">{p.localizationErrorMm !== null ? `±${p.localizationErrorMm} mm` : ''}</span>
          </div>
          <div className={cn('num grid grid-cols-3 gap-1 text-[0.8rem]', pos ? 'text-fg' : 'text-muted')}>
            <span>
              <span className="text-muted">X</span> {pos ? fmtMetres(pos.x) : '—'}
            </span>
            <span>
              <span className="text-muted">Y</span> {pos ? fmtMetres(pos.y) : '—'}
            </span>
            <span>
              <span className="text-muted">Z</span> {pos ? fmtMetres(pos.z) : '—'}
            </span>
          </div>
          <div className="text-[0.58rem] uppercase tracking-[0.12em] text-muted/80">camera + bench plane, not simulator pose</div>
        </div>
      </div>
    </Panel>
  )
}
