import type { CameraId, LabState } from '../../state/types'
import { cn } from '../../lib/format'

interface ViewportOverlaysProps {
  state: LabState
  camera: CameraId
  cameraAuto: boolean
  schematic: boolean
  live: boolean
}

const FALLBACK_LABEL: Record<CameraId, string> = {
  overview: 'WORKCELL',
  robot: 'ROBOT',
  wrist: 'WRIST',
}

/** Corner telemetry over the simulator image. Kept sparse on purpose. */
export function ViewportOverlays({ state, camera, cameraAuto, schematic, live }: ViewportOverlaysProps) {
  const { robot, run, perception, workcell } = state
  const cam = workcell.cameras.find((c) => c.id === camera)
  const box = !schematic ? perception.targetBox : null
  return (
    <div className="num pointer-events-none absolute inset-0 text-[0.72rem] tracking-[0.12em] text-fg-2 [text-shadow:0_1px_3px_rgba(0,0,0,0.95)]">
      <div className="absolute left-3 top-2.5 flex flex-col gap-0.5">
        <span className="text-fg">
          CAM: {cam?.label ?? FALLBACK_LABEL[camera]} <span className="text-muted">{cam ? `${cam.name} · ${cam.resolution}` : ''}</span>
        </span>
        {schematic ? <span className="text-[0.62rem] text-muted">SCHEMATIC · EVALUATOR GROUND TRUTH · ✛ PERCEPTION ESTIMATE</span> : null}
      </div>

      <div className="absolute right-3 top-2.5 text-right">
        <span className="text-fg">{live ? 'LIVE' : 'SIM 60 Hz'}</span>
        <span className="ml-2 text-muted">{run.simulated ? 'MUJOCO' : 'HARDWARE'}</span>
      </div>

      <div className="absolute bottom-2.5 left-3 flex flex-col gap-0.5">
        <span className="text-[0.82rem] text-fg">
          EXECUTING: {robot.fsmState}
          {robot.targetObject ? <span className="text-active"> {robot.targetObject}</span> : null}
        </span>
        <span className="text-[0.68rem] text-muted">{robot.currentAction}</span>
      </div>

      <div className="absolute bottom-2.5 right-3 text-right">
        <span className="text-fg">{run.mode === 'autonomous' ? 'AUTO' : 'MANUAL'}</span>
        <span className="ml-2 text-muted">CAM {cameraAuto ? 'AUTO' : 'FIXED'}</span>
      </div>

      {box ? (
        <div
          className={cn('absolute border border-dashed', perception.barcodeStatus === 'verified' ? 'border-ok' : 'border-active')}
          style={{ left: `${box.x * 100}%`, top: `${box.y * 100}%`, width: `${box.w * 100}%`, height: `${box.h * 100}%` }}
        >
          <span className="absolute -top-4 left-0 text-[0.66rem] text-active">
            {perception.target} {perception.confidence?.toFixed(2)}
          </span>
        </div>
      ) : null}
    </div>
  )
}
