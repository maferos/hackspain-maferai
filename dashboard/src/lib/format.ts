/** Formatting helpers shared by every readout in the console. */

/** Format a mass in grams with a fixed number of decimals. */
export function fmtMass(grams: number, digits = 3): string {
  return grams.toFixed(digits)
}

/** Format a signed delta with an explicit sign and a true minus glyph. */
export function fmtSigned(value: number, digits = 3): string {
  const sign = value < 0 ? '−' : '+'
  return `${sign}${Math.abs(value).toFixed(digits)}`
}

/** Format seconds as mm:ss. */
export function fmtClock(seconds: number): string {
  const s = Math.max(0, Math.floor(seconds))
  const mm = String(Math.floor(s / 60)).padStart(2, '0')
  const ss = String(s % 60).padStart(2, '0')
  return `${mm}:${ss}`
}

/** Format seconds as mm:ss.mmm, the resolution of the event log. */
export function fmtStamp(seconds: number): string {
  const ms = Math.max(0, Math.round(seconds * 1000))
  const mm = String(Math.floor(ms / 60000)).padStart(2, '0')
  const ss = String(Math.floor((ms % 60000) / 1000)).padStart(2, '0')
  const mmm = String(ms % 1000).padStart(3, '0')
  return `${mm}:${ss}.${mmm}`
}

/** Format a 0..1 fraction as a percentage. */
export function fmtPct(fraction: number, digits = 0): string {
  return `${(fraction * 100).toFixed(digits)}%`
}

/** Format a coordinate in metres, sign-aligned so columns line up. */
export function fmtMetres(value: number): string {
  return `${value < 0 ? '−' : ' '}${Math.abs(value).toFixed(3)}`
}

/** Join class names, dropping falsy entries. */
export function cn(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(' ')
}
