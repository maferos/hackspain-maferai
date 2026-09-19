/**
 * Runtime configuration, read once from the URL and from Vite env variables.
 *
 *   ?mode=demo|live          state source (default demo)
 *   ?url=ws://host:8765      live state endpoint (WebSocket or SSE URL)
 *   ?sim=<source>            overview camera source, see `parseViewportSource`
 *   ?simRobot=<source>       robot camera source
 *   ?simWrist=<source>       wrist camera source
 *   ?cam=overview|robot|wrist  pin a camera instead of following the robot
 *   ?speed=2                 demo playback speed
 *   ?t=95                    start the demo at that many seconds
 *   ?paused=1                start the demo paused
 *   ?loop=1                  restart the demo a few seconds after it completes
 *
 * Env defaults: VITE_LAB_URL, VITE_SIM_SOURCE, VITE_SIM_ROBOT_SOURCE,
 * VITE_SIM_WRIST_SOURCE.
 */

import type { SourceKind } from './state/sources/LabStateSource'
import type { CameraId } from './state/types'

export type ViewportSource =
  | { kind: 'schematic' }
  | { kind: 'video'; src: string }
  | { kind: 'mjpeg'; src: string }
  | { kind: 'websocket'; url: string }

/** One image source per camera of the workcell. */
export interface ViewportSources {
  overview: ViewportSource
  robot: ViewportSource
  wrist: ViewportSource
}

export interface AppConfig {
  source: SourceKind
  liveUrl: string
  viewport: ViewportSources
  /** Camera pinned at start, or null to follow the robot's active camera. */
  camera: CameraId | null
  demoSpeed: number
  /** Seconds into the demo timeline to start from. */
  demoStart: number
  demoPaused: boolean
  loop: boolean
}

const DEFAULT_LIVE_URL = 'ws://localhost:8765/state'

/**
 * Parse a viewport source spec.
 *
 *   schematic                       drawn from state (default)
 *   video:/clip.mp4 | *.mp4/*.webm  HTML video element
 *   mjpeg:http://host/stream        multipart JPEG stream in an <img>
 *   ws://host:9000/frames           JPEG/PNG frames over a WebSocket
 */
export function parseViewportSource(spec: string | null | undefined): ViewportSource {
  if (!spec || spec === 'schematic') return { kind: 'schematic' }
  if (spec.startsWith('video:')) return { kind: 'video', src: spec.slice('video:'.length) }
  if (spec.startsWith('mjpeg:')) return { kind: 'mjpeg', src: spec.slice('mjpeg:'.length) }
  if (/^wss?:\/\//.test(spec)) return { kind: 'websocket', url: spec }
  if (/\.(mp4|webm|mov)(\?.*)?$/i.test(spec)) return { kind: 'video', src: spec }
  if (/mjpe?g/i.test(spec)) return { kind: 'mjpeg', src: spec }
  return { kind: 'video', src: spec }
}

export function readConfig(): AppConfig {
  const params = new URLSearchParams(window.location.search)
  const env = import.meta.env as Record<string, string | undefined>
  const mode = params.get('mode')
  const speed = Number(params.get('speed'))
  const start = Number(params.get('t'))
  const cam = params.get('cam')
  return {
    camera: cam === 'overview' || cam === 'robot' || cam === 'wrist' ? cam : null,
    source: mode === 'live' ? 'live' : 'demo',
    liveUrl: params.get('url') ?? env.VITE_LAB_URL ?? DEFAULT_LIVE_URL,
    viewport: {
      overview: parseViewportSource(params.get('sim') ?? env.VITE_SIM_SOURCE),
      robot: parseViewportSource(params.get('simRobot') ?? env.VITE_SIM_ROBOT_SOURCE),
      wrist: parseViewportSource(params.get('simWrist') ?? env.VITE_SIM_WRIST_SOURCE),
    },
    demoSpeed: Number.isFinite(speed) && speed > 0 ? speed : 1,
    demoStart: Number.isFinite(start) && start > 0 ? start : 0,
    demoPaused: params.get('paused') === '1',
    loop: params.get('loop') === '1',
  }
}
