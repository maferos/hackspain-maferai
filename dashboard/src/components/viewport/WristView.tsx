/**
 * Eye-in-hand camera view drawn from state. Shows the label of the container
 * in front of the gripper: blurred while it is only detected, sharp once the
 * EAN-13 has been decoded, and stamped once the registry confirms the
 * identity. The bars are the real encoding of the real code.
 */

import type { LabState } from '../../state/types'
import { encodeModules } from '../../lib/ean13'
import { clamp } from '../../lib/math'
import { cn } from '../../lib/format'

const PLACEHOLDER_CODE = '2000000000000'

function Barcode({ code, decoded }: { code: string; decoded: boolean }) {
  const modules = encodeModules(code)
  const quiet = 9
  const bars: Array<{ x: number; h: number }> = []
  for (let i = 0; i < modules.length; i++) {
    if (modules[i] !== '1') continue
    const guard = i < 3 || (i >= 45 && i < 50) || i >= 92
    bars.push({ x: quiet + i, h: guard ? 54 : 48 })
  }
  return (
    <svg viewBox={`0 0 ${95 + 2 * quiet} 66`} className="block h-auto w-full" shapeRendering="crispEdges">
      {bars.map((b, i) => (
        <rect key={i} x={b.x} y={2} width={1} height={b.h} fill="#141414" />
      ))}
      <g fontFamily="var(--font-mono)" fontSize={7.5} fill="#141414" opacity={decoded ? 1 : 0.5}>
        <text x={quiet - 6} y={62}>
          {code[0]}
        </text>
        <text x={quiet + 24} y={62} textAnchor="middle" textLength={38} lengthAdjust="spacing">
          {code.slice(1, 7)}
        </text>
        <text x={quiet + 71} y={62} textAnchor="middle" textLength={38} lengthAdjust="spacing">
          {code.slice(7, 13)}
        </text>
      </g>
    </svg>
  )
}

export function WristView({ state }: { state: LabState }) {
  const p = state.perception
  const r = state.robot
  const hasTarget = p.targetIndex !== null
  const stale = hasTarget && (p.vessels.find((v) => v.index === p.targetIndex)?.stale ?? false)
  const dist = r.distanceToTarget
  const decoded = p.barcode !== null
  const verified = p.barcodeStatus === 'verified'
  const reading = p.barcodeStatus === 'reading' && !decoded
  const inHand = r.gripper !== 'open'
  const scale = hasTarget ? clamp(0.3 / Math.max(0.16, dist ?? 0.22), 0.4, 1) : 0
  const jaw = r.gripper === 'attached' ? 26 : r.gripper === 'closing' ? 18 : r.gripper === 'releasing' ? 14 : 4

  let caption = ''
  let tone = 'text-muted'
  if (!hasTarget) {
    caption = 'NO TARGET IN VIEW'
  } else if (stale) {
    caption = 'TARGET LOST · RE-DETECTING'
    tone = 'text-warn'
  } else if (verified) {
    caption = `VERIFIED · ${p.identity ?? ''} · ${p.target ?? ''}`
    tone = 'text-ok'
  } else if (decoded) {
    caption = `EAN-13 ${p.barcode} · RESOLVING`
    tone = 'text-active'
  } else if (reading) {
    caption = 'DECODING EAN-13 …'
    tone = 'text-active'
  } else if (dist !== null) {
    caption = `APPROACHING · ${dist.toFixed(2)} m`
    tone = 'text-fg-2'
  } else {
    caption = `VESSEL #${p.targetIndex} IN VIEW`
    tone = 'text-fg-2'
  }

  return (
    <div className="relative h-full w-full overflow-hidden bg-[#07090b]">
      {/* Vignette and bench texture */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,#161b22_0%,#0b0e12_60%,#05070a_100%)]" />

      {/* Gripper fingers, visible at the frame edges of an eye-in-hand camera */}
      <div className="absolute inset-y-[18%] w-[9%] bg-[#1b2129] shadow-[inset_-2px_0_0_#2c3540] transition-[left] duration-500" style={{ left: `${jaw - 8}%` }} />
      <div className="absolute inset-y-[18%] w-[9%] bg-[#1b2129] shadow-[inset_2px_0_0_#2c3540] transition-[right] duration-500" style={{ right: `${jaw - 8}%` }} />

      {/* Reticle */}
      <div className="pointer-events-none absolute inset-0 flex items-center justify-center">
        <div className="size-[46%] border border-line-2/70" />
        <div className="absolute h-px w-[6%] bg-line-2" />
        <div className="absolute h-[9%] w-px bg-line-2" />
      </div>

      {/* Label */}
      {hasTarget ? (
        <div
          className="absolute left-1/2 top-1/2 w-[48%] transition-transform duration-500"
          style={{ transform: `translate(-50%, -50%) scale(${scale}) rotate(${inHand ? 0 : -2.5}deg)`, opacity: stale ? 0.35 : 1 }}
        >
          <div
            className={cn('rounded-[3px] bg-[#efe9dc] px-[5%] pb-[4%] pt-[3%] text-[#141414] shadow-[0_10px_30px_rgba(0,0,0,0.6)] transition-[filter] duration-300', !decoded && 'blur-[2.2px]')}
          >
            <div className="flex items-baseline justify-between text-[0.62rem] font-semibold tracking-[0.18em]">
              <span>MAFERAI LAB · SAMPLE</span>
              <span className="num">{verified ? p.target : '—'}</span>
            </div>
            <div className="mt-[3%] border-t border-[#c9c1b0] pt-[3%]">
              <Barcode code={p.barcode ?? PLACEHOLDER_CODE} decoded={decoded} />
            </div>
            <div className="mt-[2%] text-center text-[1rem] font-bold tracking-[0.22em]">{p.identity ? p.identity.toUpperCase() : '••••••••'}</div>
          </div>
          {reading ? (
            <div className="pointer-events-none absolute inset-0 overflow-hidden">
              <div className="animate-scanline h-[3px] w-full bg-active/80 shadow-[0_0_12px_2px_rgba(61,196,222,0.6)]" />
            </div>
          ) : null}
          {decoded ? <div className={cn('pointer-events-none absolute -inset-1 border', verified ? 'border-ok' : 'border-active')} /> : null}
        </div>
      ) : null}

      <div className={cn('num absolute bottom-9 left-1/2 -translate-x-1/2 text-[0.78rem] tracking-[0.14em]', tone)}>{caption}</div>
    </div>
  )
}
