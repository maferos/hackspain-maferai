import { useLabState } from '../state/LabStateProvider'
import { fmtMetres } from '../lib/format'
import { Panel } from './ui/Panel'
import { KeyValue } from './ui/KeyValue'

const GRIPPER_TONE = {
  open: 'muted',
  closing: 'active',
  attached: 'ok',
  releasing: 'active',
} as const

/** Compact engineering telemetry of the arm and the planner state. */
export function RobotTelemetry() {
  const { state } = useLabState()
  const { robot, perception } = state
  const barcodeLabel = perception.barcodeStatus === 'verified' ? 'VERIFIED' : perception.barcodeStatus === 'reading' ? 'READING' : perception.barcodeStatus === 'mismatch' ? 'MISMATCH' : '—'
  const barcodeTone = perception.barcodeStatus === 'verified' ? 'ok' : perception.barcodeStatus === 'reading' ? 'active' : perception.barcodeStatus === 'mismatch' ? 'warn' : 'muted'
  const right = <span className="num text-[0.72rem] tracking-[0.12em] text-active">{robot.fsmState}</span>

  return (
    <Panel title="Robot state" right={right} bodyClassName="flex flex-col px-2.5 py-1.5">
      <div className="grid flex-1 grid-cols-[1.15fr_1fr_1fr] gap-x-4">
        <div>
          <KeyValue label="State" value={robot.fsmState} tone="active" size="lg" />
          <KeyValue label="Arm" value={robot.arm} />
          <KeyValue label="End effector" value={robot.endEffector} />
          <KeyValue label="Target" value={robot.targetObject ?? '—'} tone={robot.targetObject ? 'default' : 'muted'} />
          <KeyValue label="Compound" value={robot.compound ?? '—'} tone={robot.compound ? 'default' : 'muted'} />
          <KeyValue label="Base x" value={`${fmtMetres(robot.basePosition.x)} m`} />
        </div>
        <div>
          <div className="text-[0.62rem] uppercase tracking-[0.12em] text-muted">EE position</div>
          <KeyValue label="X" value={`${fmtMetres(robot.eePosition.x)} m`} size="md" />
          <KeyValue label="Y" value={`${fmtMetres(robot.eePosition.y)} m`} size="md" />
          <KeyValue label="Z" value={`${fmtMetres(robot.eePosition.z)} m`} size="md" />
          <KeyValue label="Gripper" value={robot.gripper.toUpperCase()} tone={GRIPPER_TONE[robot.gripper]} />
          <KeyValue label="Tilt" value={`${robot.tiltDeg.toFixed(1)}°`} tone={robot.tiltDeg > 0 ? 'active' : 'muted'} />
        </div>
        <div>
          <KeyValue label="Detection" value={perception.confidence !== null ? perception.confidence.toFixed(2) : '—'} tone={perception.confidence !== null ? 'default' : 'muted'} />
          <KeyValue label="Barcode" value={barcodeLabel} tone={barcodeTone} />
          <KeyValue label="Localization" value={perception.localizationErrorMm !== null ? `±${perception.localizationErrorMm} mm` : '—'} tone={perception.localizationErrorMm !== null ? 'default' : 'muted'} />
          <KeyValue label="Distance" value={robot.distanceToTarget !== null ? `${robot.distanceToTarget.toFixed(3)} m` : '—'} tone={robot.distanceToTarget !== null ? 'default' : 'muted'} />
          <KeyValue label="IK error" value={`${robot.ikErrorMm.toFixed(1)} mm`} className="secondary" />
          <KeyValue label="Recoveries" value={String(robot.recoveries)} tone={robot.recoveries > 0 ? 'warn' : 'default'} />
        </div>
      </div>
      <div className="mt-1 flex items-center gap-2 border-t border-line pt-1.5">
        <span className="shrink-0 text-[0.62rem] uppercase tracking-[0.12em] text-muted">Current action</span>
        <span className="min-w-0 flex-1 truncate text-[0.88rem] text-fg">{robot.currentAction}</span>
        <span className="relative h-1 w-16 shrink-0 overflow-hidden bg-line">
          {state.run.status === 'running' ? <span className="animate-activity absolute inset-y-0 w-1/3 bg-active/70" /> : null}
        </span>
      </div>
    </Panel>
  )
}
