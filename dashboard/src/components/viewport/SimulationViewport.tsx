/**
 * Main viewport. Shows one camera of the workcell from whichever source is
 * configured for it (schematic drawn from state, video, MJPEG or WebSocket
 * frames) and layers the telemetry overlays on top. The camera follows the
 * robot's active camera unless the operator pins one.
 */

import { useState } from 'react'
import type { CameraId } from '../../state/types'
import type { ViewportSources } from '../../config'
import { useLabState } from '../../state/LabStateProvider'
import { cn } from '../../lib/format'
import { Panel } from '../ui/Panel'
import { SchematicView } from './SchematicView'
import { WristView } from './WristView'
import { StreamView } from './StreamView'
import { ViewportOverlays } from './ViewportOverlays'
import { CompletionBanner } from './CompletionBanner'

const CAMERAS: Array<[CameraId, string]> = [
  ['overview', 'Overview'],
  ['robot', 'Robot'],
  ['wrist', 'Wrist cam'],
]

interface SimulationViewportProps {
  sources: ViewportSources
  /** Camera pinned at start; null follows the robot's active camera. */
  initialCamera?: CameraId | null
}

export function SimulationViewport({ sources, initialCamera = null }: SimulationViewportProps) {
  const { state, source: stateSource } = useLabState()
  const [pinned, setPinned] = useState<CameraId | null>(initialCamera)
  const camera: CameraId = pinned ?? state.perception.activeCamera
  const source = sources[camera]
  const schematic = source.kind === 'schematic'

  const controls = (
    <div className="flex items-center gap-0.5 text-[0.66rem] font-semibold tracking-[0.14em]">
      {CAMERAS.map(([id, label]) => (
        <button
          key={id}
          type="button"
          onClick={() => setPinned(id)}
          className={cn('px-2 py-0.5 uppercase', camera === id ? 'bg-panel-3 text-fg' : 'text-muted hover:text-fg-2')}
        >
          {label}
        </button>
      ))}
      <span className="mx-1 h-3.5 w-px bg-line-2" />
      <button
        type="button"
        onClick={() => setPinned(null)}
        className={cn('px-2 py-0.5', pinned === null ? 'text-active' : 'text-muted hover:text-fg-2')}
        title="Follow the camera the robot is using"
      >
        AUTO
      </button>
    </div>
  )

  return (
    <Panel title="Simulation / Workcell" right={controls} bodyClassName="bg-black">
      <div className="absolute inset-0">
        {schematic ? camera === 'wrist' ? <WristView state={state} /> : <SchematicView state={state} camera={camera} /> : <StreamView source={source} />}
      </div>
      <ViewportOverlays state={state} camera={camera} cameraAuto={pinned === null} schematic={schematic} live={stateSource === 'live'} />
      {state.summary ? <CompletionBanner summary={state.summary} /> : null}
    </Panel>
  )
}
