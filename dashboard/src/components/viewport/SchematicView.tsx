/**
 * Schematic workcell drawn from state, used when no simulator stream is
 * attached. Furniture comes from `state.workcell`, object poses from
 * `state.evaluator` (simulator ground truth, labelled as such) and the
 * perception overlay is drawn separately from `state.perception`, so the two
 * never blend. Top-down view, X along the bench, aisle at the bottom.
 */

import type { LabState } from '../../state/types'
import { clamp } from '../../lib/math'

interface SchematicViewProps {
  state: LabState
  camera: 'overview' | 'robot'
}

const ROBOT_WINDOW_W = 3.6
const REACH = 0.85
const RADIUS: Record<string, number> = { 'amber bottle': 0.02, 'hdpe bottle': 0.032 }

export function SchematicView({ state, camera }: SchematicViewProps) {
  const wc = state.workcell
  const p = state.perception
  const r = state.robot
  const bench = wc.bench
  const railY = wc.rail?.y ?? r.basePosition.y
  const base = r.basePosition
  const ee = r.eePosition

  const view =
    camera === 'overview'
      ? { x0: bench.x0 - 0.3, x1: bench.x1 + 0.3, y0: Math.min(railY, bench.y0) - 0.42, y1: bench.y1 + 0.3 }
      : (() => {
          const cx = clamp(base.x, bench.x0 + ROBOT_WINDOW_W / 2 - 0.3, bench.x1 - ROBOT_WINDOW_W / 2 + 0.3)
          return { x0: cx - ROBOT_WINDOW_W / 2, x1: cx + ROBOT_WINDOW_W / 2, y0: Math.min(railY, bench.y0) - 0.3, y1: bench.y1 + 0.1 }
        })()
  const W = (view.x1 - view.x0) * 1000
  const H = (view.y1 - view.y0) * 1000
  const px = (x: number) => (x - view.x0) * 1000
  const py = (y: number) => (view.y1 - y) * 1000
  const mm = (m: number) => m * 1000
  // Text is sized against whichever axis limits the fit, so labels stay ~12 px.
  const font = Math.max(W / 92, H / 50)

  // Two-link planar projection of the arm, bent away from the straight line.
  const dx = ee.x - base.x
  const dy = ee.y - base.y
  const d = Math.hypot(dx, dy) || 1e-6
  const bend = 0.05 + 0.18 * (1 - Math.min(1, d / REACH))
  const elbow = { x: base.x + dx * 0.5 - (dy / d) * bend, y: base.y + dy * 0.5 + (dx / d) * bend }

  const target = p.targetIndex !== null ? p.vessels.find((v) => v.index === p.targetIndex) ?? null : null
  const pouring = r.tiltDeg > 30
  const held = state.evaluator?.groundTruth.find((g) => g.tiltDeg > 0 || (r.gripper === 'attached' && g.index === p.targetIndex)) ?? null
  const activeBalance = wc.balances.find((b) => b.active) ?? null

  return (
    <svg viewBox={`0 0 ${W} ${H}`} className="h-full w-full" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Schematic workcell">
      <defs>
        <pattern id="bench-grid" width="250" height="250" patternUnits="userSpaceOnUse" x={px(0)} y={py(0)}>
          <path d="M 250 0 L 0 0 0 250" fill="none" stroke="#1c2229" strokeWidth={1} vectorEffect="non-scaling-stroke" />
        </pattern>
      </defs>

      {/* Bench */}
      <rect x={px(bench.x0)} y={py(bench.y1)} width={mm(bench.x1 - bench.x0)} height={mm(bench.y1 - bench.y0)} fill="#11151a" />
      <rect x={px(bench.x0)} y={py(bench.y1)} width={mm(bench.x1 - bench.x0)} height={mm(bench.y1 - bench.y0)} fill="url(#bench-grid)" stroke="#2c3540" strokeWidth={1} vectorEffect="non-scaling-stroke" />
      {/* Gantry along the spine */}
      <line x1={px(bench.x0)} x2={px(bench.x1)} y1={py(0)} y2={py(0)} stroke="#2c3540" strokeWidth={3} vectorEffect="non-scaling-stroke" opacity={0.8} />
      <text x={px(bench.x0) + 14} y={py(0) - 8} fontSize={font * 0.75} fill="#5c6774" fontFamily="var(--font-mono)">
        GANTRY
      </text>
      <text x={px(bench.x0) + 14} y={py(bench.y0) - 10} fontSize={font * 0.75} fill="#5c6774" fontFamily="var(--font-mono)">
        BENCH {(bench.x1 - bench.x0).toFixed(1)} × {(bench.y1 - bench.y0).toFixed(1)} m · z = {bench.top.toFixed(2)} m
      </text>

      {/* Rail */}
      {wc.rail ? (
        <g>
          <line x1={px(wc.rail.x0)} x2={px(wc.rail.x1)} y1={py(wc.rail.y)} y2={py(wc.rail.y)} stroke="#3a4450" strokeWidth={4} vectorEffect="non-scaling-stroke" />
          <line x1={px(wc.rail.x0)} x2={px(wc.rail.x1)} y1={py(wc.rail.y)} y2={py(wc.rail.y)} stroke="#1c2229" strokeWidth={1} strokeDasharray="2 8" vectorEffect="non-scaling-stroke" />
          <text x={px(wc.rail.x0)} y={py(wc.rail.y) + font * 1.3} fontSize={font * 0.75} fill="#5c6774" fontFamily="var(--font-mono)">
            RAIL {wc.rail.x0.toFixed(1)} … {wc.rail.x1.toFixed(1)} m
          </text>
        </g>
      ) : null}

      {/* Balances */}
      {wc.balances.map((b) => {
        const active = b.active
        const fill = active ? Math.min(1, state.balance.totalMass / Math.max(0.001, state.balance.batchTargetMass)) : 0
        return (
          <g key={b.id} transform={`translate(${px(b.position.x)} ${py(b.position.y)})`}>
            <rect x={-mm(0.11)} y={-mm(0.13)} width={mm(0.22)} height={mm(0.26)} fill={active ? '#171c22' : '#13181d'} stroke={active ? '#6b7684' : '#2c3540'} strokeWidth={1} vectorEffect="non-scaling-stroke" />
            <circle r={mm(0.036)} fill="#0f1215" stroke={active ? '#6b7684' : '#3a4450'} strokeWidth={1.2} vectorEffect="non-scaling-stroke" />
            {active ? <circle r={mm(0.036) * fill} fill="#b5762b" opacity={0.5} /> : null}
            <text y={-mm(0.13) - font * 0.4} textAnchor="middle" fontSize={font * 0.75} fill={active ? '#98a2ae' : '#5c6774'} fontFamily="var(--font-mono)">
              {b.id.toUpperCase()}
            </text>
          </g>
        )
      })}

      {/* Robot: carriage, base, reach */}
      <circle cx={px(base.x)} cy={py(base.y)} r={mm(REACH)} fill="none" stroke="#2c3540" strokeWidth={1} strokeDasharray="6 6" vectorEffect="non-scaling-stroke" opacity={0.7} />
      <rect x={px(base.x - 0.16)} y={py(base.y + 0.11)} width={mm(0.32)} height={mm(0.22)} fill="#151a20" stroke="#3a4450" strokeWidth={1} vectorEffect="non-scaling-stroke" />
      <circle cx={px(base.x)} cy={py(base.y)} r={mm(0.075)} fill="#1a2028" stroke="#3a4450" strokeWidth={1.2} vectorEffect="non-scaling-stroke" />
      <text x={px(base.x)} y={py(base.y) + font * 1.9} textAnchor="middle" fontSize={font * 0.75} fill="#98a2ae" fontFamily="var(--font-mono)">
        {r.arm.toUpperCase()} · x {base.x.toFixed(2)}
      </text>

      {/* Arm */}
      <polyline
        points={`${px(base.x)},${py(base.y)} ${px(elbow.x)},${py(elbow.y)} ${px(ee.x)},${py(ee.y)}`}
        fill="none"
        stroke="#98a2ae"
        strokeWidth={5}
        strokeLinecap="round"
        strokeLinejoin="round"
        vectorEffect="non-scaling-stroke"
      />
      <circle cx={px(elbow.x)} cy={py(elbow.y)} r={mm(0.018)} fill="#0f1215" stroke="#98a2ae" strokeWidth={2} vectorEffect="non-scaling-stroke" />

      {/* Ground-truth vessels (evaluator) */}
      {state.evaluator?.groundTruth.map((g) => {
        const perceived = p.vessels.find((v) => v.index === g.index)
        const cls = perceived?.cls ?? 'amber bottle'
        const rad = RADIUS[cls] ?? 0.022
        const amber = cls === 'amber bottle'
        const label = perceived?.id ?? `#${g.index}`
        const isHeld = held?.index === g.index
        const tilt = g.tiltDeg
        return (
          <g key={g.index} transform={`translate(${px(g.position.x)} ${py(g.position.y)})`}>
            <ellipse
              rx={mm(rad) * (1 + tilt / 90)}
              ry={mm(rad)}
              transform={`rotate(${-tilt})`}
              fill={amber ? '#5a3a15' : '#3a3f46'}
              stroke={amber ? '#b5762b' : '#aab2bc'}
              strokeWidth={1.4}
              vectorEffect="non-scaling-stroke"
            />
            {!isHeld ? (
              <text y={-mm(rad) - font * 0.45} textAnchor="middle" fontSize={font * 0.78} fill={perceived?.id ? '#d6dce4' : '#98a2ae'} fontFamily="var(--font-mono)">
                {label}
              </text>
            ) : null}
          </g>
        )
      })}

      {/* Pour stream */}
      {pouring && held && activeBalance ? (
        <line x1={px(held.position.x)} y1={py(held.position.y)} x2={px(activeBalance.position.x)} y2={py(activeBalance.position.y)} stroke="#b5762b" strokeWidth={2} strokeDasharray="3 5" vectorEffect="non-scaling-stroke" opacity={0.8} />
      ) : null}

      {/* End effector */}
      <g transform={`translate(${px(ee.x)} ${py(ee.y)})`}>
        <circle r={mm(0.03)} fill="none" stroke="#3dc4de" strokeWidth={1.5} vectorEffect="non-scaling-stroke" />
        <line x1={-mm(0.045)} x2={mm(0.045)} y1={0} y2={0} stroke="#3dc4de" strokeWidth={1} vectorEffect="non-scaling-stroke" />
        <line y1={-mm(0.045)} y2={mm(0.045)} x1={0} x2={0} stroke="#3dc4de" strokeWidth={1} vectorEffect="non-scaling-stroke" />
        <text x={mm(0.05)} y={-mm(0.035)} fontSize={font * 0.75} fill="#3dc4de" fontFamily="var(--font-mono)">
          EE z {ee.z.toFixed(3)}
        </text>
      </g>

      {/* Perception overlay: estimates and the current target */}
      {p.vessels.map((v) => (
        <g key={`est-${v.index}`} transform={`translate(${px(v.position.x)} ${py(v.position.y)})`} opacity={v.stale ? 0.5 : 0.85}>
          <line x1={-mm(0.012)} x2={mm(0.012)} y1={0} y2={0} stroke={v.stale ? '#d29922' : '#3dc4de'} strokeWidth={1.2} vectorEffect="non-scaling-stroke" />
          <line y1={-mm(0.012)} y2={mm(0.012)} x1={0} x2={0} stroke={v.stale ? '#d29922' : '#3dc4de'} strokeWidth={1.2} vectorEffect="non-scaling-stroke" />
        </g>
      ))}
      {target ? (
        <g transform={`translate(${px(target.position.x)} ${py(target.position.y)})`}>
          <rect x={-mm(0.06)} y={-mm(0.06)} width={mm(0.12)} height={mm(0.12)} fill="none" stroke={target.stale ? '#d29922' : '#3dc4de'} strokeWidth={1.2} strokeDasharray="5 4" vectorEffect="non-scaling-stroke" />
          <text x={mm(0.07)} y={mm(0.07)} fontSize={font * 0.78} fill={target.stale ? '#d29922' : '#3dc4de'} fontFamily="var(--font-mono)">
            {target.stale ? `${p.target ?? ''} STALE` : `${p.target ?? ''} ${target.confidence.toFixed(2)}`}
          </text>
        </g>
      ) : null}
      {target && r.distanceToTarget !== null && !target.stale ? (
        <line x1={px(ee.x)} y1={py(ee.y)} x2={px(target.position.x)} y2={py(target.position.y)} stroke="#3dc4de" strokeWidth={1} strokeDasharray="2 6" vectorEffect="non-scaling-stroke" opacity={0.6} />
      ) : null}
    </svg>
  )
}
