/**
 * Closed-loop dosing profile used by the demo timeline.
 *
 * Mirrors the controller design of the formulation lab: FAST until the
 * remaining mass is small, SLOW to approach the target, PULSE to land inside
 * tolerance, then STOP and wait for a stable reading. The profile is a pure
 * function of time since the dose started, so the demo is deterministic.
 * Powders flow more slowly than liquids and pulse in smaller steps.
 */

import type { DosingMode, Phase } from '../types'
import { wobble } from '../../lib/math'

export interface DoseProfile {
  target: number
  /** Mass on the balance when the dose ends (target plus the scripted error). */
  final: number
  rateFast: number
  rateSlow: number
  /** Time spent in each phase, seconds. */
  tFast: number
  tSlow: number
  tPulse: number
  pulses: number
  pulseMass: number
  pulsePeriod: number
  /** Total length of the dose segment. */
  duration: number
  massAt(u: number): number
  modeAt(u: number): DosingMode
  flowAt(u: number): number
  tiltAt(u: number): number
  stableAt(u: number): boolean
}

const RATES: Record<Phase, { fast: number; slow: number; pulse: number }> = {
  liquid: { fast: 0.42, slow: 0.084, pulse: 0.018 },
  powder: { fast: 0.34, slow: 0.07, pulse: 0.014 },
}
const PULSE_PERIOD = 0.7
const PULSE_RAMP = 0.15
const PULSE_LEAD = 0.15
const FAST_HANDOVER = 0.55
const SLOW_HANDOVER = 0.06

export function makeDoseProfile(target: number, error: number, phase: Phase = 'liquid'): DoseProfile {
  const rates = RATES[phase]
  const mFast = Math.max(target * 0.5, target - FAST_HANDOVER)
  const mSlow = target - SLOW_HANDOVER
  const tFast = mFast / rates.fast
  const tSlow = (mSlow - mFast) / rates.slow
  const remaining = target + error - mSlow
  const pulses = Math.max(1, Math.round(remaining / rates.pulse))
  const pulseMass = remaining / pulses
  const tPulse = pulses * PULSE_PERIOD + 0.5
  const duration = tFast + tSlow + tPulse
  const final = target + error

  const pulseStart = (k: number) => tFast + tSlow + k * PULSE_PERIOD + PULSE_LEAD

  const massAt = (u: number): number => {
    if (u <= 0) return 0
    if (u < tFast) return rates.fast * u
    if (u < tFast + tSlow) return mFast + rates.slow * (u - tFast)
    let m = mSlow
    for (let k = 0; k < pulses; k++) {
      const t0 = pulseStart(k)
      if (u >= t0) m += pulseMass * Math.min(1, (u - t0) / PULSE_RAMP)
    }
    return Math.min(m, final)
  }

  const modeAt = (u: number): DosingMode => {
    if (u < tFast) return 'fast'
    if (u < tFast + tSlow) return 'slow'
    if (u < duration) return 'pulse'
    return 'stopped'
  }

  /** Seconds since the most recent pulse started, or +inf before the first. */
  const sinceLastPulse = (u: number): number => {
    let s = Number.POSITIVE_INFINITY
    for (let k = 0; k < pulses; k++) {
      const t0 = pulseStart(k)
      if (u >= t0) s = u - t0
    }
    return s
  }

  const flowAt = (u: number): number => {
    switch (modeAt(u)) {
      case 'fast':
        return rates.fast + 0.05 * rates.fast * wobble(u, 1)
      case 'slow':
        return rates.slow + 0.05 * rates.slow * wobble(u, 2)
      case 'pulse':
        return pulseMass / PULSE_PERIOD
      default:
        return 0
    }
  }

  const tiltAt = (u: number): number => {
    switch (modeAt(u)) {
      case 'fast':
        return (phase === 'powder' ? 58.0 : 52.0) + 0.8 * wobble(u, 3)
      case 'slow':
        return (phase === 'powder' ? 44.0 : 37.2) + 0.3 * wobble(u, 4)
      case 'pulse': {
        const s = sinceLastPulse(u)
        const inPulse = s < PULSE_RAMP + 0.1
        return inPulse ? (phase === 'powder' ? 48.0 : 41.5) : (phase === 'powder' ? 34.0 : 28.0)
      }
      default:
        return 0
    }
  }

  const stableAt = (u: number): boolean => {
    const mode = modeAt(u)
    if (mode === 'fast' || mode === 'slow') return false
    if (mode === 'pulse') return sinceLastPulse(u) > 0.45
    return true
  }

  return {
    target,
    final,
    rateFast: rates.fast,
    rateSlow: rates.slow,
    tFast,
    tSlow,
    tPulse,
    pulses,
    pulseMass,
    pulsePeriod: PULSE_PERIOD,
    duration,
    massAt,
    modeAt,
    flowAt,
    tiltAt,
    stableAt,
  }
}
