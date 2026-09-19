/**
 * Demo source: replays the deterministic timeline in wall-clock time.
 *
 * It owns the playback clock (play, pause, speed, seek) and publishes
 * `demoStateAt(t)` at a fixed rate. Nothing about the recipe lives here.
 */

import type { LabState } from '../types'
import type { ConnectionListener, DemoControls, LabStateSource, StateListener } from './LabStateSource'
import { DEMO_DURATION, demoStateAt } from '../demo/timeline'

const TICK_MS = 66

export class DemoSource implements LabStateSource, DemoControls {
  readonly kind = 'demo' as const
  readonly duration = DEMO_DURATION

  private listeners = new Set<StateListener>()
  private connListeners = new Set<ConnectionListener>()
  private timer: number | null = null
  private position = 0
  private lastTick = 0
  private state: LabState | null = null
  private isPlaying = false
  private multiplier = 1
  private startPaused: boolean
  /** Seconds of pause at the end before the demo loops, or null to hold. */
  private loopAfter: number | null

  constructor(options: { loopAfterSeconds?: number | null; speed?: number; startAt?: number; paused?: boolean } = {}) {
    this.loopAfter = options.loopAfterSeconds ?? null
    this.multiplier = options.speed ?? 1
    this.position = Math.max(0, Math.min(this.duration, options.startAt ?? 0))
    this.startPaused = options.paused ?? false
  }

  get playing(): boolean {
    return this.isPlaying
  }

  get speed(): number {
    return this.multiplier
  }

  start(): void {
    if (this.timer !== null) return
    this.lastTick = performance.now()
    this.isPlaying = !this.startPaused
    this.publish()
    this.timer = window.setInterval(() => this.tick(), TICK_MS)
    this.connListeners.forEach((l) => l('open'))
  }

  stop(): void {
    if (this.timer !== null) window.clearInterval(this.timer)
    this.timer = null
    this.isPlaying = false
    this.connListeners.forEach((l) => l('closed'))
  }

  subscribe(listener: StateListener): () => void {
    this.listeners.add(listener)
    if (this.state) listener(this.state)
    return () => this.listeners.delete(listener)
  }

  subscribeConnection(listener: ConnectionListener): () => void {
    this.connListeners.add(listener)
    listener(this.timer !== null ? 'open' : 'idle')
    return () => this.connListeners.delete(listener)
  }

  current(): LabState | null {
    return this.state
  }

  play(): void {
    this.lastTick = performance.now()
    this.isPlaying = true
    this.publish()
  }

  pause(): void {
    this.isPlaying = false
    this.publish()
  }

  restart(): void {
    this.position = 0
    this.lastTick = performance.now()
    this.isPlaying = true
    this.publish()
  }

  seek(seconds: number): void {
    this.position = Math.max(0, Math.min(this.duration, seconds))
    this.publish()
  }

  setSpeed(multiplier: number): void {
    this.multiplier = multiplier
    this.publish()
  }

  private tick(): void {
    const now = performance.now()
    if (this.isPlaying) {
      this.position += ((now - this.lastTick) / 1000) * this.multiplier
      if (this.position >= this.duration) {
        if (this.loopAfter !== null && this.position >= this.duration + this.loopAfter) {
          this.position = 0
        }
      }
    }
    this.lastTick = now
    this.publish()
  }

  private publish(): void {
    this.state = demoStateAt(this.position)
    this.listeners.forEach((l) => l(this.state as LabState))
  }
}
