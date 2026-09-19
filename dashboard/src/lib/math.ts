/** Small numeric helpers used by the demo timeline and the schematic view. */

import type { Vec3 } from '../state/types'

export function clamp(x: number, lo: number, hi: number): number {
  return Math.min(hi, Math.max(lo, x))
}

export function lerp(a: number, b: number, u: number): number {
  return a + (b - a) * u
}

/** Cubic ease used for every motion in the demo so nothing moves linearly. */
export function smoothstep(u: number): number {
  const x = clamp(u, 0, 1)
  return x * x * (3 - 2 * x)
}

export function lerpVec(a: Vec3, b: Vec3, u: number): Vec3 {
  return { x: lerp(a.x, b.x, u), y: lerp(a.y, b.y, u), z: lerp(a.z, b.z, u) }
}

export function distance(a: Vec3, b: Vec3): number {
  return Math.hypot(a.x - b.x, a.y - b.y, a.z - b.z)
}

/**
 * Deterministic, smooth pseudo-noise in [-1, 1]. The demo uses it for
 * measurement jitter so a replay always looks the same.
 */
export function wobble(t: number, seed = 0): number {
  return Math.sin(t * 7.3 + seed) * Math.sin(t * 2.1 + seed * 0.7) * Math.cos(t * 11.9 + seed * 1.3)
}

/** Round to a number of decimals; balances quantise their reading. */
export function quantise(x: number, digits: number): number {
  const f = 10 ** digits
  return Math.round(x * f) / f
}
