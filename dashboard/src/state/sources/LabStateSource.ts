/**
 * Data-transport abstraction.
 *
 * A source publishes `LabState` snapshots. The UI subscribes through
 * `LabStateProvider` and never knows whether the snapshots come from the
 * scripted demo or from the real system over a socket.
 */

import type { LabState } from '../types'

export type SourceKind = 'demo' | 'live'

export type ConnectionStatus = 'idle' | 'connecting' | 'open' | 'closed' | 'error'

export type StateListener = (state: LabState) => void
export type ConnectionListener = (status: ConnectionStatus) => void

export interface LabStateSource {
  readonly kind: SourceKind
  /** Start producing state. Safe to call more than once. */
  start(): void
  /** Stop producing state and release resources. */
  stop(): void
  subscribe(listener: StateListener): () => void
  subscribeConnection(listener: ConnectionListener): () => void
  /** Last published state, if any. */
  current(): LabState | null
}

/** Playback controls offered by the demo source only. */
export interface DemoControls {
  play(): void
  pause(): void
  restart(): void
  seek(seconds: number): void
  setSpeed(multiplier: number): void
  readonly playing: boolean
  readonly speed: number
  readonly duration: number
}
