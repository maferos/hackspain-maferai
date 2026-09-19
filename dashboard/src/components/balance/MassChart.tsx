/**
 * Scrolling mass-over-time chart. One series (net mass on the balance) with
 * the target as a labelled reference line, so the closed-loop approach to the
 * target is visible: fast rise, slower approach, pulses, settle.
 */

import { useState } from 'react'
import type { MassSample } from '../../state/types'
import { useSize } from '../../lib/useSize'
import { fmtMass } from '../../lib/format'

interface MassChartProps {
  history: MassSample[]
  target: number
  window: number
  now: number
}

const PAD = { left: 38, right: 8, top: 10, bottom: 18 }

export function MassChart({ history, target, window: windowSeconds, now }: MassChartProps) {
  const [ref, size] = useSize<HTMLDivElement>()
  const [hover, setHover] = useState<number | null>(null)
  const W = size.width
  const H = size.height
  const innerW = Math.max(1, W - PAD.left - PAD.right)
  const innerH = Math.max(1, H - PAD.top - PAD.bottom)

  const maxMass = history.reduce((m, s) => Math.max(m, s.mass), 0)
  const yMax = Math.max(target * 1.15, maxMass * 1.05, 0.05)
  const t0 = now - windowSeconds
  const x = (t: number) => PAD.left + ((t - t0) / windowSeconds) * innerW
  const y = (m: number) => PAD.top + innerH - (m / yMax) * innerH

  const visible = history.filter((s) => s.time >= t0 - 1e-6)
  const points = visible.map((s) => `${x(s.time).toFixed(1)},${y(s.mass).toFixed(1)}`).join(' ')
  const last = visible[visible.length - 1]
  const area = last ? `${points} ${x(last.time).toFixed(1)},${y(0).toFixed(1)} ${x(visible[0].time).toFixed(1)},${y(0).toFixed(1)}` : ''

  const hovered = hover !== null && visible.length ? visible.reduce((best, s) => (Math.abs(x(s.time) - hover) < Math.abs(x(best.time) - hover) ? s : best), visible[0]) : null
  const gridSteps = [0.25, 0.5, 0.75, 1]

  return (
    <div
      ref={ref}
      className="relative h-full w-full"
      onMouseMove={(e) => setHover(e.clientX - e.currentTarget.getBoundingClientRect().left)}
      onMouseLeave={() => setHover(null)}
    >
      {W > 0 && H > 0 ? (
        <svg width={W} height={H} className="block" role="img" aria-label="Net mass over the last seconds against the target">
          {gridSteps.map((g) => (
            <line key={g} x1={PAD.left} x2={W - PAD.right} y1={y(yMax * g)} y2={y(yMax * g)} stroke="#1f252d" strokeWidth={1} />
          ))}
          <line x1={PAD.left} x2={W - PAD.right} y1={y(0)} y2={y(0)} stroke="#2c3540" strokeWidth={1} />

          <text x={PAD.left - 6} y={y(0) + 3} textAnchor="end" fontSize={10} fill="#5c6774" fontFamily="var(--font-mono)">
            0
          </text>
          <text x={PAD.left - 6} y={y(yMax) + 4} textAnchor="end" fontSize={10} fill="#5c6774" fontFamily="var(--font-mono)">
            {yMax.toFixed(1)}
          </text>
          <text x={PAD.left} y={H - 5} fontSize={10} fill="#5c6774" fontFamily="var(--font-mono)">
            {'−'}
            {windowSeconds} s
          </text>
          <text x={W - PAD.right} y={H - 5} textAnchor="end" fontSize={10} fill="#5c6774" fontFamily="var(--font-mono)">
            now
          </text>

          {target > 0 ? (
            <g>
              <line x1={PAD.left} x2={W - PAD.right} y1={y(target)} y2={y(target)} stroke="#98a2ae" strokeWidth={1} strokeDasharray="4 4" />
              <text x={W - PAD.right} y={y(target) - 4} textAnchor="end" fontSize={10} fill="#98a2ae" fontFamily="var(--font-mono)">
                target {fmtMass(target)} g
              </text>
            </g>
          ) : null}

          {visible.length > 1 ? (
            <g>
              <polygon points={area} fill="#3dc4de" opacity={0.08} />
              <polyline points={points} fill="none" stroke="#3dc4de" strokeWidth={2} strokeLinejoin="round" strokeLinecap="round" />
            </g>
          ) : null}
          {last ? (
            <g>
              <circle cx={x(last.time)} cy={y(last.mass)} r={5} fill="#0f1215" />
              <circle cx={x(last.time)} cy={y(last.mass)} r={3.5} fill="#3dc4de" />
            </g>
          ) : null}

          {hovered ? (
            <g>
              <line x1={x(hovered.time)} x2={x(hovered.time)} y1={PAD.top} y2={y(0)} stroke="#2c3540" strokeWidth={1} />
              <circle cx={x(hovered.time)} cy={y(hovered.mass)} r={4} fill="#0f1215" stroke="#d6dce4" strokeWidth={1.5} />
            </g>
          ) : null}
        </svg>
      ) : null}
      {hovered ? (
        <div
          className="num pointer-events-none absolute top-1 border border-line-2 bg-panel-2 px-1.5 py-0.5 text-[0.68rem] text-fg"
          style={{ left: Math.min(Math.max(0, x(hovered.time) - 48), Math.max(0, W - 104)) }}
        >
          {(hovered.time - now).toFixed(1)} s {'·'} {fmtMass(hovered.mass)} g
        </div>
      ) : null}
    </div>
  )
}
