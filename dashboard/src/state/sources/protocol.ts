/**
 * Live message protocol.
 *
 * The real system (simulation loop, planner, balance) publishes JSON messages
 * over a WebSocket or Server-Sent Events. Three shapes are accepted:
 *
 *  - `snapshot`      full `LabState`, replaces everything
 *  - `state_update`  deep partial of `LabState` under `patch`, merged in; or a
 *                    flat legacy update with `robot_state`, `step`,
 *                    `balance_g`, `target_g`
 *  - `event`         one log line, appended
 *  - `mass_sample`   one balance sample, appended to the chart history
 *
 * Anything else is ignored, so a producer can add message types freely.
 */

import type { DeepPartial, EventLevel, LabEvent, LabState } from '../types'

export interface SnapshotMessage {
  type: 'snapshot'
  timestamp?: number
  state: LabState
}

export interface StateUpdateMessage {
  type: 'state_update'
  timestamp?: number
  patch?: DeepPartial<LabState>
  /* Flat legacy fields, kept for simple producers. */
  robot_state?: string
  step?: string
  balance_g?: number
  target_g?: number
  elapsed_s?: number
  progress?: number
}

export interface EventMessage {
  type: 'event'
  time: number
  message: string
  level?: EventLevel
}

export interface MassSampleMessage {
  type: 'mass_sample'
  time: number
  mass: number
}

export type LiveMessage = SnapshotMessage | StateUpdateMessage | EventMessage | MassSampleMessage

const MAX_EVENTS = 50
const MAX_HISTORY = 600

function isObject(x: unknown): x is Record<string, unknown> {
  return typeof x === 'object' && x !== null && !Array.isArray(x)
}

/** Deep merge where arrays and primitives in the patch replace the base. */
export function deepMerge<T>(base: T, patch: DeepPartial<T> | undefined): T {
  if (patch === undefined) return base
  if (!isObject(base) || !isObject(patch)) return patch as T
  const out: Record<string, unknown> = { ...base }
  for (const [k, v] of Object.entries(patch)) {
    if (v === undefined) continue
    out[k] = isObject(v) && isObject(out[k]) ? deepMerge(out[k], v) : v
  }
  return out as T
}

let eventSeq = 0

/** Apply one live message to the current state, returning the new state. */
export function applyMessage(state: LabState, msg: LiveMessage): LabState {
  switch (msg.type) {
    case 'snapshot':
      return msg.state
    case 'state_update': {
      let next = msg.patch ? deepMerge(state, msg.patch) : state
      const flat: DeepPartial<LabState> = {}
      if (msg.robot_state !== undefined) flat.robot = { fsmState: msg.robot_state }
      if (msg.step !== undefined) flat.execution = { currentStepId: msg.step }
      if (msg.balance_g !== undefined || msg.target_g !== undefined) {
        flat.balance = {}
        if (msg.balance_g !== undefined) flat.balance.netMass = msg.balance_g
        if (msg.target_g !== undefined) flat.balance.targetMass = msg.target_g
      }
      if (msg.elapsed_s !== undefined || msg.progress !== undefined) {
        flat.run = {}
        if (msg.elapsed_s !== undefined) flat.run.elapsedSeconds = msg.elapsed_s
        if (msg.progress !== undefined) flat.run.progress = msg.progress
      }
      next = deepMerge(next, flat)
      if (msg.balance_g !== undefined) {
        const time = msg.elapsed_s ?? next.run.elapsedSeconds
        next = { ...next, balance: { ...next.balance, history: pushSample(next.balance.history, { time, mass: msg.balance_g }) } }
      }
      return next
    }
    case 'event': {
      const ev: LabEvent = { id: `live-${eventSeq++}`, time: msg.time, message: msg.message, level: msg.level ?? 'info' }
      return { ...state, events: [...state.events, ev].slice(-MAX_EVENTS) }
    }
    case 'mass_sample':
      return { ...state, balance: { ...state.balance, history: pushSample(state.balance.history, { time: msg.time, mass: msg.mass }) } }
    default:
      return state
  }
}

function pushSample(history: LabState['balance']['history'], sample: { time: number; mass: number }) {
  return [...history, sample].slice(-MAX_HISTORY)
}

/** Parse a raw socket payload; returns null for anything that is not a message. */
export function parseMessage(raw: string): LiveMessage | null {
  try {
    const parsed: unknown = JSON.parse(raw)
    if (isObject(parsed) && typeof parsed.type === 'string') return parsed as unknown as LiveMessage
  } catch {
    /* malformed payloads are ignored */
  }
  return null
}
