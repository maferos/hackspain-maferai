/**
 * Deterministic demo timeline.
 *
 * `compile()` turns the demo recipe into a list of timed segments (locate,
 * traverse the rail, approach, read barcode, ..., dose, return) plus the
 * events they emit. `demoStateAt(t)` then derives the complete `LabState` for
 * any instant, so the demo can be paused, sped up or scrubbed and always looks
 * the same. Geometry comes from `recipe.ts`, i.e. from the simulation scene.
 */

import type {
  CameraId,
  DosingMode,
  EventLevel,
  ExecutionStep,
  GripperState,
  Ingredient,
  LabEvent,
  LabState,
  MacroPhase,
  ModuleStatus,
  PerceivedVessel,
  PipelineNodeState,
  StepStatus,
  Vec3,
} from '../types'
import { clamp, distance, lerp, lerpVec, quantise, smoothstep, wobble } from '../../lib/math'
import { fmtMass, fmtSigned } from '../../lib/format'
import {
  DEMO_RECIPE,
  DEMO_RUN_ID,
  DISPLACEMENT,
  FORMULATION_BALANCE,
  POUR_POSE,
  ROBOT,
  VESSELS,
  WORKCELL,
  cameraFor,
  vesselByIndex,
  type DemoIngredient,
} from './recipe'
import { makeDoseProfile, type DoseProfile } from './dosing'

type SegmentKind =
  | 'parse'
  | 'detect'
  | 'locate'
  | 'traverse'
  | 'approach'
  | 'recover'
  | 'barcode'
  | 'verify'
  | 'pick'
  | 'toBalance'
  | 'dose'
  | 'settle'
  | 'return'
  | 'validate'
  | 'complete'

interface Keyframe {
  /** Fraction of the segment (0..1] at which the end effector reaches `pos`. */
  at: number
  pos: Vec3
}

interface Segment {
  kind: SegmentKind
  start: number
  end: number
  ingredient: number | null
  stepId: string | null
  attempt: number
  eeStart: Vec3
  /** Keyframes after the start; empty means the arm holds its pose. */
  path: Keyframe[]
  /** Rail position of the arm base at the start and end of the segment. */
  baseStart: number
  baseEnd: number
  /** Fraction window of the segment during which the carriage travels. */
  baseWindow: [number, number]
  dose: DoseProfile | null
}

interface StepSpec {
  id: string
  label: string
  ingredientId: string | null
}

interface Timeline {
  segments: Segment[]
  steps: StepSpec[]
  stepSegments: Map<string, Segment[]>
  events: LabEvent[]
  duration: number
  /** When the Eugenol flask is displaced, and when it is reacquired. */
  displacementTime: number
  reacquireTime: number
}

const HISTORY_WINDOW = 30
const HISTORY_STEP = 0.2
const LOCATE_ERROR_MM = 11
const HOVER_Z = 1.1
const READ_Z = 1.06
const GRASP_Z = 0.965
const LIFT_Z = 1.12

const above = (p: Vec3, z: number): Vec3 => ({ x: p.x, y: p.y, z })
const basePos = (x: number): Vec3 => ({ x, y: ROBOT.baseY, z: ROBOT.baseZ })
const carryPose = (x: number): Vec3 => ({ x, y: ROBOT.baseY + ROBOT.carry.dy, z: ROBOT.baseZ + ROBOT.carry.dz })
const travelTime = (from: number, to: number) => Math.abs(to - from) / ROBOT.railSpeed

function compile(): Timeline {
  const R = DEMO_RECIPE
  const segments: Segment[] = []
  const steps: StepSpec[] = []
  const stepSegments = new Map<string, Segment[]>()
  const events: LabEvent[] = []
  let t = 0
  let ee = carryPose(ROBOT.homeX)
  let base = ROBOT.homeX
  let seq = 0
  let displacementTime = 0
  let reacquireTime = 0

  const event = (time: number, message: string, level: EventLevel = 'info') => {
    events.push({ id: `ev-${seq++}`, time, message, level })
  }

  const step = (id: string, label: string, ingredientId: string | null = null) => {
    steps.push({ id, label, ingredientId })
    return id
  }

  const seg = (
    kind: SegmentKind,
    duration: number,
    opts: {
      ingredient?: number
      stepId?: string
      attempt?: number
      path?: Keyframe[]
      baseEnd?: number
      baseWindow?: [number, number]
      dose?: DoseProfile
    } = {},
  ): Segment => {
    const s: Segment = {
      kind,
      start: t,
      end: t + duration,
      ingredient: opts.ingredient ?? null,
      stepId: opts.stepId ?? null,
      attempt: opts.attempt ?? 1,
      eeStart: ee,
      path: opts.path ?? [],
      baseStart: base,
      baseEnd: opts.baseEnd ?? base,
      baseWindow: opts.baseWindow ?? [0, 1],
      dose: opts.dose ?? null,
    }
    segments.push(s)
    if (s.stepId) {
      const list = stepSegments.get(s.stepId) ?? []
      list.push(s)
      stepSegments.set(s.stepId, list)
    }
    t = s.end
    ee = s.path.length ? s.path[s.path.length - 1].pos : ee
    base = s.baseEnd
    return s
  }

  const n = R.ingredients.length

  // Recipe-level start.
  seg('parse', 1.2, { stepId: step('parse', 'Parse formulation') })
  event(0.0, `recipe ${R.id} received: ${R.name}, ${n} ingredients, ${fmtMass(R.targetMass)} g`)
  event(0.9, `formulation parsed: ${n} ingredients queued, vessel on ${FORMULATION_BALANCE.id}`, 'ok')

  const overview = cameraFor('overview')
  const d = seg('detect', 2.6, { stepId: step('detect', 'Detect candidate containers') })
  event(d.start + 0.2, `${overview.name} camera: frame ${overview.resolution} acquired`)
  event(d.start + 1.5, `detector: ${VESSELS.length} vessels (amber bottle ×${VESSELS.filter((v) => v.cls === 'amber bottle').length}, hdpe bottle ×${VESSELS.filter((v) => v.cls === 'hdpe bottle').length})`)
  event(d.start + 2.3, `bench-plane localization: ${VESSELS.length} candidates ±12 mm`, 'ok')

  let total = 0
  R.ingredients.forEach((ing: DemoIngredient, i: number) => {
    const v = vesselByIndex(ing.vesselIndex)
    const displaced = ing.vesselIndex === DISPLACEMENT.vesselIndex
    const targetPos = displaced ? DISPLACEMENT.to : v.position
    const sid = (name: string) => `${name}-${ing.id}`
    const c = ing.container

    const s1 = seg('locate', 1.6, { ingredient: i, stepId: step(sid('locate'), `Locate candidate · ${ing.compound}`, ing.id) })
    event(s1.start + 0.2, `planner: candidate vessel #${v.index} for ${ing.compound} (${v.position.x.toFixed(2)}, ${v.position.y.toFixed(2)})`)
    event(s1.start + 1.1, `pose estimated ±${v.localizationErrorMm} mm`)

    // Ride the rail until the container is within reach.
    if (Math.abs(base - v.position.x) > 0.05) {
      const dur = travelTime(base, v.position.x) + 0.8
      const tr = seg('traverse', dur, {
        ingredient: i,
        stepId: step(sid('traverse'), `Traverse rail → x ${v.position.x.toFixed(2)} m`, ing.id),
        path: [
          { at: 0.05, pos: carryPose(base) },
          { at: 0.95, pos: carryPose(v.position.x) },
        ],
        baseEnd: v.position.x,
        baseWindow: [0.05, 0.95],
      })
      event(tr.start + 0.1, `rail: traverse ${Math.abs(v.position.x - tr.baseStart).toFixed(2)} m to x = ${v.position.x.toFixed(2)}`)
    }

    step(sid('approach'), `Approach vessel #${v.index}`, ing.id)
    if (displaced) {
      const partial = lerpVec(ee, above(v.position, HOVER_Z), 0.45)
      const a1 = seg('approach', 1.4, { ingredient: i, stepId: sid('approach'), path: [{ at: 1, pos: partial }] })
      event(a1.start + 0.1, `IK: approach vessel #${v.index}`)
      const rc = seg('recover', 2.6, { ingredient: i, stepId: sid('approach'), attempt: 1 })
      displacementTime = rc.start
      reacquireTime = rc.start + 2.1
      const moved = distance(v.position, DISPLACEMENT.to)
      event(rc.start, `target displaced: vessel #${v.index} moved ${(moved * 100).toFixed(1)} cm`, 'warn')
      event(rc.start + 0.3, 'pose invalidated, motion cancelled', 'warn')
      event(rc.start + 0.9, 'replanning: re-detect target from wrist camera')
      event(reacquireTime, `target reacquired (${DISPLACEMENT.to.x.toFixed(2)}, ${DISPLACEMENT.to.y.toFixed(2)}) ±12 mm`, 'ok')
      const a2 = seg('approach', 3.0, { ingredient: i, stepId: sid('approach'), attempt: 2, path: [{ at: 1, pos: above(targetPos, HOVER_Z) }] })
      event(a2.start + 0.1, `IK: approach vessel #${v.index} (attempt 2)`)
      event(a2.end - 0.3, 'wrist camera: label in view')
    } else {
      const a = seg('approach', 3.2, { ingredient: i, stepId: sid('approach'), path: [{ at: 1, pos: above(targetPos, HOVER_Z) }] })
      event(a.start + 0.1, `IK: approach vessel #${v.index}`)
      event(a.end - 0.3, 'wrist camera: label in view')
    }

    const b = seg('barcode', 1.8, { ingredient: i, stepId: step(sid('barcode'), 'Read barcode · wrist camera', ing.id), path: [{ at: 1, pos: above(targetPos, READ_Z) }] })
    event(b.start + 1.1, `barcode read: ${c.barcode} (EAN-13)`)

    const vf = seg('verify', 0.7, { ingredient: i, stepId: step(sid('verify'), `Verify identity · ${ing.compound}`, ing.id) })
    event(vf.start + 0.4, `identity verified: ${c.id} = ${ing.compound}, ${c.ml} mL ${ing.phase}`, 'ok')

    const pk = seg('pick', 2.4, {
      ingredient: i,
      stepId: step(sid('pick'), `Pick ${c.id}`, ing.id),
      path: [
        { at: 0.35, pos: above(targetPos, GRASP_Z) },
        { at: 0.6, pos: above(targetPos, GRASP_Z) },
        { at: 1, pos: above(targetPos, LIFT_Z) },
      ],
    })
    event(pk.start + 1.45, `grasp attached: ${c.id}`, 'ok')

    // Carry the container to the formulation balance, riding the rail if needed.
    const toTravel = travelTime(base, POUR_POSE.x)
    const mv = seg('toBalance', 2.4 + toTravel, {
      ingredient: i,
      stepId: step(sid('move'), `Move to ${FORMULATION_BALANCE.id} · tare`, ing.id),
      path: [
        { at: 0.15, pos: carryPose(base) },
        { at: 0.85, pos: carryPose(POUR_POSE.x) },
        { at: 1, pos: POUR_POSE },
      ],
      baseEnd: POUR_POSE.x,
      baseWindow: [0.15, 0.85],
    })
    event(mv.start + 0.2, toTravel > 0.1 ? `rail: carry ${c.id} ${Math.abs(POUR_POSE.x - mv.baseStart).toFixed(2)} m to ${FORMULATION_BALANCE.id}` : 'IK: move to pour pose over balance')
    event(mv.end - 0.1, 'balance tared')

    const dose = makeDoseProfile(ing.targetMass, ing.doseError, ing.phase)
    const ds = seg('dose', dose.duration, { ingredient: i, stepId: step(sid('dose'), `Dose ${ing.compound}`, ing.id), dose })
    event(ds.start, `dosing started: ${ing.compound} (${ing.phase}), target ${fmtMass(ing.targetMass)} g (FAST)`)
    event(ds.start + dose.tFast, 'controller switched FAST → SLOW')
    event(ds.start + dose.tFast + dose.tSlow, 'controller switched SLOW → PULSE')
    event(ds.end - 0.4, 'flow stopped, waiting for stable reading')
    total += dose.final

    const st = seg('settle', 1.6, { ingredient: i, stepId: step(sid('mass'), 'Verify mass', ing.id) })
    event(st.start + 1.2, `mass verified: ${fmtMass(dose.final)} g (Δ ${fmtSigned(ing.doseError)} g) PASS`, 'ok')

    const backTravel = travelTime(base, targetPos.x)
    const rt = seg('return', 3.4 + backTravel, {
      ingredient: i,
      stepId: step(sid('return'), `Return ${c.id}`, ing.id),
      path: [
        { at: 0.12, pos: carryPose(base) },
        { at: 0.6, pos: carryPose(targetPos.x) },
        { at: 0.72, pos: above(targetPos, LIFT_Z) },
        { at: 0.82, pos: above(targetPos, GRASP_Z) },
        { at: 0.9, pos: above(targetPos, GRASP_Z) },
        { at: 1, pos: above(targetPos, LIFT_Z) },
      ],
      baseEnd: targetPos.x,
      baseWindow: [0.12, 0.6],
    })
    event(rt.start + 0.2, `return ${c.id} to bench`)
    event(rt.start + (3.4 + backTravel) * 0.88, `container released: ${c.id}`)
  })

  const homeTravel = travelTime(base, ROBOT.homeX)
  const va = seg('validate', 2.2 + homeTravel, {
    stepId: step('validate', 'Validate final mass'),
    path: [
      { at: 0.1, pos: carryPose(base) },
      { at: 0.9, pos: carryPose(ROBOT.homeX) },
    ],
    baseEnd: ROBOT.homeX,
    baseWindow: [0.1, 0.9],
  })
  event(va.start + 1.5, `final mass ${fmtMass(total)} g, target ${fmtMass(R.targetMass)} g, error ${fmtMass(Math.abs(total - R.targetMass))} g: PASS`, 'ok')

  const cp = seg('complete', 0.8, { stepId: step('complete', 'Complete formulation') })
  event(cp.start + 0.1, 'formulation complete', 'ok')

  return { segments, steps, stepSegments, events, duration: t, displacementTime, reacquireTime }
}

const TL: Timeline = compile()

/** Total length of the demo in seconds. */
export const DEMO_DURATION = TL.duration

function segmentIndexAt(t: number): number {
  const segs = TL.segments
  if (t >= TL.duration) return segs.length - 1
  for (let i = 0; i < segs.length; i++) if (t < segs[i].end) return i
  return segs.length - 1
}

function eeAt(seg: Segment, u: number): Vec3 {
  if (!seg.path.length) return seg.eeStart
  let prevAt = 0
  let prevPos = seg.eeStart
  for (const k of seg.path) {
    if (u <= k.at) {
      const span = k.at - prevAt
      const f = span > 0 ? (u - prevAt) / span : 1
      return lerpVec(prevPos, k.pos, smoothstep(f))
    }
    prevAt = k.at
    prevPos = k.pos
  }
  return seg.path[seg.path.length - 1].pos
}

function baseAt(seg: Segment, u: number): number {
  const [a, b] = seg.baseWindow
  const f = b > a ? (u - a) / (b - a) : 1
  return lerp(seg.baseStart, seg.baseEnd, smoothstep(f))
}

const FSM: Record<SegmentKind, string> = {
  parse: 'LOAD_RECIPE',
  detect: 'SCAN_SCENE',
  locate: 'LOCATE',
  traverse: 'TRAVERSE',
  approach: 'APPROACH',
  recover: 'RECOVER',
  barcode: 'READ_BARCODE',
  verify: 'VERIFY_ID',
  pick: 'PICK',
  toBalance: 'MOVE_TO_POUR',
  dose: 'DOSING',
  settle: 'VERIFY_MASS',
  return: 'RETURN_BOTTLE',
  validate: 'VALIDATE',
  complete: 'COMPLETE',
}

const CAMERA: Record<SegmentKind, CameraId> = {
  parse: 'overview',
  detect: 'overview',
  locate: 'overview',
  traverse: 'robot',
  approach: 'wrist',
  recover: 'wrist',
  barcode: 'wrist',
  verify: 'wrist',
  pick: 'wrist',
  toBalance: 'robot',
  dose: 'robot',
  settle: 'robot',
  return: 'wrist',
  validate: 'overview',
  complete: 'overview',
}

const MOVING: ReadonlySet<SegmentKind> = new Set(['traverse', 'approach', 'pick', 'toBalance', 'return', 'validate'])
const HANDLING: ReadonlySet<SegmentKind> = new Set(['locate', 'traverse', 'approach', 'recover', 'barcode', 'verify', 'pick', 'toBalance', 'dose', 'settle', 'return'])

function macroPhase(kind: SegmentKind, local: number): MacroPhase {
  switch (kind) {
    case 'parse':
      return 'plan'
    case 'detect':
    case 'locate':
      return 'perceive'
    case 'recover':
      return local < 0.9 ? 'perceive' : local < 2.1 ? 'plan' : 'perceive'
    case 'barcode':
    case 'verify':
      return 'identify'
    case 'traverse':
    case 'approach':
    case 'pick':
    case 'toBalance':
    case 'return':
      return 'move'
    case 'dose':
      return 'dose'
    default:
      return 'verify'
  }
}

function gripperAt(kind: SegmentKind, u: number): GripperState {
  switch (kind) {
    case 'pick':
      return u < 0.35 ? 'open' : u < 0.6 ? 'closing' : 'attached'
    case 'toBalance':
    case 'dose':
    case 'settle':
      return 'attached'
    case 'return':
      return u < 0.82 ? 'attached' : u < 0.9 ? 'releasing' : 'open'
    default:
      return 'open'
  }
}

/** Net mass on the balance (since the last tare) at absolute time `tau`. */
function netMassAt(tau: number): { net: number; flowing: boolean } {
  if (tau < 0) return { net: 0, flowing: false }
  const seg = TL.segments[segmentIndexAt(tau)]
  if (seg.kind === 'dose' && seg.dose) {
    const u = tau - seg.start
    return { net: seg.dose.massAt(u), flowing: seg.dose.flowAt(u) > 0 }
  }
  let last = 0
  for (const s of TL.segments) {
    if (s.kind === 'dose' && s.dose && s.end <= tau) last = s.dose.final
  }
  return { net: last, flowing: false }
}

function readingAt(tau: number): number {
  const { net, flowing } = netMassAt(tau)
  const noise = flowing ? 0.0025 * wobble(tau, 9) : 0
  return quantise(Math.max(0, net + noise), 3)
}

/** Which ingredient the balance readout refers to at time `t`. */
function balanceIngredientIndex(seg: Segment, t: number): number | null {
  if (seg.ingredient !== null && (seg.kind === 'toBalance' || seg.kind === 'dose' || seg.kind === 'settle' || seg.kind === 'return')) {
    return seg.ingredient
  }
  let last: number | null = null
  for (const s of TL.segments) if (s.kind === 'dose' && s.end <= t) last = s.ingredient
  return last
}

export function demoStateAt(rawT: number): LabState {
  const R = DEMO_RECIPE
  const t = clamp(rawT, 0, TL.duration)
  const completed = rawT >= TL.duration
  const seg = TL.segments[segmentIndexAt(t)]
  const local = t - seg.start
  const u = clamp(local / (seg.end - seg.start), 0, 1)
  const ing = seg.ingredient !== null ? R.ingredients[seg.ingredient] : null
  const vessel = ing ? vesselByIndex(ing.vesselIndex) : null
  const ee = eeAt(seg, u)
  const baseX = baseAt(seg, u)
  const gripper = gripperAt(seg.kind, u)
  const displacedNow = t >= TL.displacementTime
  const reacquired = t >= TL.reacquireTime

  // ---- Ground truth (evaluator) -----------------------------------------
  const truthPos = (index: number): Vec3 => {
    const v = vesselByIndex(index)
    return index === DISPLACEMENT.vesselIndex && displacedNow ? DISPLACEMENT.to : v.position
  }
  const heldIndex = ing && gripper !== 'open' && gripper !== 'closing' ? ing.vesselIndex : null
  const tilt = seg.kind === 'dose' && seg.dose ? seg.dose.tiltAt(local) : seg.kind === 'settle' ? lerp(28, 0, smoothstep(local / 0.5)) : 0
  const groundTruth = VESSELS.map((v) => ({
    index: v.index,
    body: v.body,
    position: v.index === heldIndex ? { x: ee.x, y: ee.y, z: ee.z - 0.07 } : truthPos(v.index),
    tiltDeg: v.index === heldIndex ? tilt : 0,
  }))

  // ---- Identity knowledge (what the robot has verified so far) ----------
  const verifiedAt = new Map<number, number>()
  for (const s of TL.segments) {
    if (s.kind === 'verify' && s.ingredient !== null && s.end <= t) {
      verifiedAt.set(R.ingredients[s.ingredient].vesselIndex, s.end)
    }
  }
  const currentVerified = ing ? verifiedAt.has(ing.vesselIndex) : false

  // ---- Perception -------------------------------------------------------
  const detectSeg = TL.segments[1]
  const detectFraction = t < detectSeg.start ? 0 : smoothstep(clamp((t - detectSeg.start) / 2.0, 0, 1))
  const detections = Math.round(detectFraction * VESSELS.length)
  const perceivedVessels: PerceivedVessel[] = VESSELS.slice(0, detections).map((v) => {
    const isDisplaced = v.index === DISPLACEMENT.vesselIndex
    const stale = isDisplaced && displacedNow && !reacquired
    const base = isDisplaced && reacquired ? DISPLACEMENT.to : v.position
    const known = R.ingredients.find((x) => x.vesselIndex === v.index)
    return {
      index: v.index,
      id: known && verifiedAt.has(v.index) ? known.container.id : null,
      cls: v.cls,
      confidence: v.confidence,
      position: { x: base.x + v.estimateOffset.x, y: base.y + v.estimateOffset.y, z: base.z },
      stale,
    }
  })
  const targetVessel = ing && HANDLING.has(seg.kind) ? perceivedVessels.find((p) => p.index === ing.vesselIndex) ?? null : null
  const barcodeKnown =
    ing &&
    ((seg.kind === 'barcode' && local >= 1.1) ||
      (seg.kind !== 'barcode' && seg.kind !== 'locate' && seg.kind !== 'traverse' && seg.kind !== 'approach' && seg.kind !== 'recover' && HANDLING.has(seg.kind)))
  const barcodeStatus = !ing || !HANDLING.has(seg.kind)
    ? 'idle'
    : seg.kind === 'barcode'
      ? 'reading'
      : seg.kind === 'verify'
        ? local < 0.4 ? 'reading' : 'verified'
        : currentVerified
          ? 'verified'
          : 'idle'
  const camera = CAMERA[seg.kind]
  const cam = cameraFor(camera)
  const targetName = ing && targetVessel ? (currentVerified ? ing.container.id : `vessel #${ing.vesselIndex}`) : null

  const modules = {
    detector: (seg.kind === 'detect' || seg.kind === 'locate' || (seg.kind === 'recover' && local >= 0.9) ? 'active' : 'ok') as ModuleStatus,
    localizer: (seg.kind === 'locate' ? 'active' : seg.kind === 'recover' && local < 2.1 ? 'warn' : 'ok') as ModuleStatus,
    barcode: (seg.kind === 'barcode' ? 'active' : barcodeStatus === 'verified' ? 'ok' : 'idle') as ModuleStatus,
    wristCam: (camera === 'wrist' ? 'active' : 'idle') as ModuleStatus,
  }

  // ---- Balance ----------------------------------------------------------
  const reading = readingAt(t)
  let doseMode: DosingMode = 'stopped'
  let flow = 0
  let stable = true
  if (seg.kind === 'dose' && seg.dose) {
    doseMode = seg.dose.modeAt(local)
    flow = seg.dose.flowAt(local)
    stable = seg.dose.stableAt(local)
  } else if (seg.kind === 'settle') {
    stable = local > 0.8
  }
  let totalMass = 0
  for (const s of TL.segments) {
    if (s.kind !== 'dose' || !s.dose) continue
    if (s.end <= t) totalMass += s.dose.final
    else if (s.start <= t) totalMass += s.dose.massAt(t - s.start)
  }
  const balIdx = balanceIngredientIndex(seg, t)
  const balIng = balIdx !== null ? R.ingredients[balIdx] : R.ingredients[0]
  const history = []
  for (let tau = t - HISTORY_WINDOW; tau <= t + 1e-9; tau += HISTORY_STEP) {
    history.push({ time: tau, mass: readingAt(tau) })
  }

  // ---- Execution steps --------------------------------------------------
  const steps: ExecutionStep[] = TL.steps.map((spec) => {
    const segs = TL.stepSegments.get(spec.id) ?? []
    const first = segs[0]
    const last = segs[segs.length - 1]
    const containing = segs.find((s) => s.start <= t && t < s.end) ?? null
    let status: StepStatus = 'queued'
    if (completed || (last && last.end <= t)) status = 'completed'
    else if (containing) status = containing.kind === 'recover' ? 'retrying' : 'active'
    const attempt = containing ? containing.attempt : last ? last.attempt : 1
    const detail: Array<[string, string]> = []
    if (containing && status !== 'completed') {
      switch (containing.kind) {
        case 'recover':
          detail.push(['recovery', 'target displaced → replanning'], ['attempt', `${attempt + 1} of 3`])
          break
        case 'traverse':
          detail.push(['rail x', `${baseX.toFixed(2)} m`], ['speed', `${ROBOT.railSpeed.toFixed(2)} m/s`])
          break
        case 'approach':
          if (vessel) detail.push(['distance', `${distance(ee, truthPos(vessel.index)).toFixed(2)} m`])
          if (attempt > 1) detail.push(['attempt', `${attempt} of 3`])
          break
        case 'barcode':
          detail.push(['camera', `${cam.name} ${cam.resolution}`], ['symbology', 'EAN-13'])
          break
        case 'verify':
          if (ing) detail.push(['code', ing.container.barcode], ['registry', 'lookup_table.json'])
          break
        case 'pick':
          detail.push(['gripper', gripper.toUpperCase()])
          break
        case 'toBalance':
          detail.push(['rail x', `${baseX.toFixed(2)} m`], ['balance', FORMULATION_BALANCE.id])
          break
        case 'dose':
          detail.push(['target', `${fmtMass(balIng.targetMass)} g`], ['current', `${fmtMass(reading)} g`], ['mode', doseMode.toUpperCase()], ['flow', `${flow.toFixed(3)} g/s`])
          break
        case 'settle':
          detail.push(['reading', `${fmtMass(reading)} g`], ['stable', stable ? 'YES' : 'settling'])
          break
        case 'detect':
          detail.push(['detections', `${detections}`])
          break
        default:
          break
      }
    }
    return {
      id: spec.id,
      label: spec.label,
      ingredientId: spec.ingredientId,
      status,
      attempt,
      startedAt: first && first.start <= t ? first.start : null,
      completedAt: status === 'completed' && last ? last.end : null,
      detail,
    }
  })

  // ---- Ingredients ------------------------------------------------------
  const ingredients: Ingredient[] = R.ingredients.map((x, i) => {
    const own = TL.segments.filter((s) => s.ingredient === i)
    const done = completed || own[own.length - 1].end <= t
    const active = !done && own.some((s) => s.start <= t && t < s.end)
    const doseSeg = own.find((s) => s.kind === 'dose')
    let dispensed: number | null = null
    if (doseSeg && doseSeg.dose) {
      if (doseSeg.end <= t) dispensed = doseSeg.dose.final
      else if (doseSeg.start <= t) dispensed = reading
    }
    const verified = verifiedAt.has(x.vesselIndex)
    return {
      id: x.id,
      compound: x.compound,
      cas: x.cas,
      phase: x.phase,
      targetMass: x.targetMass,
      dispensedMass: dispensed,
      containerId: verified ? x.container.id : null,
      containerMl: verified ? x.container.ml : null,
      status: done ? 'completed' : active ? 'active' : 'queued',
    }
  })

  // ---- Robot ------------------------------------------------------------
  const moving = MOVING.has(seg.kind)
  const ikError = moving ? 0.9 + 1.2 * Math.abs(wobble(t, 5)) : 0.3
  const targetTruth = vessel ? truthPos(vessel.index) : null
  const distToTarget = targetTruth && (seg.kind === 'approach' || seg.kind === 'recover' || seg.kind === 'barcode' || seg.kind === 'verify' || seg.kind === 'pick') ? distance(ee, targetTruth) : null
  const recoveries = TL.segments.filter((s) => s.kind === 'recover' && s.start <= t).length
  const action = ((): string => {
    switch (seg.kind) {
      case 'parse':
        return `Load recipe ${R.id}`
      case 'detect':
        return `${cam.name} camera: detect containers`
      case 'locate':
        return `Select candidate for ${ing?.compound ?? ''}`
      case 'traverse':
        return `Rail → x ${seg.baseEnd.toFixed(2)} m · now ${baseX.toFixed(2)} m`
      case 'approach':
        return `Approach vessel #${ing?.vesselIndex ?? ''} · ${(distToTarget ?? 0).toFixed(2)} m`
      case 'recover':
        return local < 0.9 ? 'Motion cancelled: target displaced' : local < 2.1 ? 'Replanning: re-detect target' : 'Target reacquired'
      case 'barcode':
        return 'Wrist camera: read label'
      case 'verify':
        return 'Resolve barcode in sample registry'
      case 'pick':
        return u < 0.35 ? 'Descend to grasp height' : u < 0.6 ? 'Close gripper' : 'Lift container'
      case 'toBalance':
        return u < 0.85 ? `Carry to ${FORMULATION_BALANCE.id} · rail x ${baseX.toFixed(2)} m` : 'Move to pour pose'
      case 'dose':
        return `Tilt container → ${tilt.toFixed(1)}°`
      case 'settle':
        return 'Level container · wait for stable reading'
      case 'return':
        return u < 0.6 ? `Carry container back · rail x ${baseX.toFixed(2)} m` : u < 0.82 ? 'Descend to place' : u < 0.9 ? 'Open gripper' : 'Retract'
      case 'validate':
        return 'Validate final formulation mass'
      default:
        return 'Idle · formulation complete'
    }
  })()

  // ---- Pipeline ---------------------------------------------------------
  const passed = ingredients.filter((x) => x.status === 'completed').length
  const pipeline: PipelineNodeState[] = [
    {
      id: 'camera',
      title: 'Camera',
      model: camera === 'wrist' ? 'Wrist RGB' : `${cam.label} RGB`,
      lines: [`${cam.resolution} · 30 fps`, `scene cam ${cam.name}`],
      status: seg.kind === 'detect' || seg.kind === 'approach' || seg.kind === 'barcode' || seg.kind === 'recover' ? 'active' : 'ok',
      details: [
        ['general', 'GoPro Linear 1080p, f = 927 px, fixed at (-1.5, -2.9, 3.0)'],
        ['wrist', '1280×720 RGB, eye-in-hand'],
        ['camera pose', 'forward kinematics + hand-eye calibration'],
        ['frame', 'scene world frame, worktop z = 0.90 m'],
      ],
    },
    {
      id: 'detection',
      title: 'Object detection',
      model: 'YOLO11s',
      lines: [`${(13 + 2 * Math.abs(wobble(t, 6))).toFixed(0)} ms · 640 px`, `${detections} detections`],
      status: modules.detector === 'active' ? 'active' : 'ok',
      details: [
        ['weights', 'yolo11s, fine-tuned on simulator renders'],
        ['classes', 'amber bottle · hdpe bottle · vessel'],
        ['input', '640 px letterbox'],
        ['confidence threshold', '0.25'],
        ['nms iou', '0.60'],
      ],
    },
    {
      id: 'localization',
      title: '3D localization',
      model: 'Bench-plane ray',
      lines: [targetVessel ? `±${vessel?.localizationErrorMm ?? LOCATE_ERROR_MM} mm` : `±${LOCATE_ERROR_MM} mm`, `${detections} candidates`],
      status: modules.localizer,
      details: [
        ['method', 'pinhole ray ∩ bench plane (z = 0.90 m)'],
        ['anchor', 'bottom edge of the detection box'],
        ['intrinsics', 'f = 927 px (general), calibrated'],
        ['uncertainty', '±11 mm at 1.2 m, grows with distance'],
      ],
    },
    {
      id: 'barcode',
      title: 'Barcode ID',
      model: 'EAN-13',
      lines: [barcodeKnown && ing ? ing.container.barcode : '—', barcodeStatus === 'verified' ? 'VERIFIED' : barcodeStatus === 'reading' ? 'READING' : 'IDLE'],
      status: modules.barcode,
      details: [
        ['symbology', 'EAN-13, GS1 internal prefix 200'],
        ['registry', 'lookup_table.json, 200 samples'],
        ['min symbol width', '190 px at 1280 px'],
        ['read distance', '≤ 0.30 m, wrist camera only'],
      ],
    },
    {
      id: 'planner',
      title: 'Task planner',
      model: 'FSM',
      lines: [`STATE ${FSM[seg.kind]}`, `replans ${recoveries}`],
      status: seg.kind === 'parse' || seg.kind === 'locate' || (seg.kind === 'recover' && local >= 0.9 && local < 2.1) ? 'active' : 'ok',
      details: [
        ['states', 'SCAN → LOCATE → TRAVERSE → APPROACH → READ → VERIFY → PICK → POUR → DOSE → VERIFY → RETURN'],
        ['tick', '100 Hz, non-blocking generators'],
        ['world model', 'change threshold 2 cm / 15°'],
        ['recovery', 'displaced → relocate; mismatch → next candidate'],
      ],
    },
    {
      id: 'motion',
      title: 'Motion',
      model: 'IK · mink',
      lines: [moving ? 'TRACKING' : 'HOLD', `err ${ikError.toFixed(1)} mm · rail ${baseX.toFixed(2)}`],
      status: moving ? 'active' : 'ok',
      details: [
        ['arm', `${ROBOT.arm}, 7 DOF on a linear rail`],
        ['solver', 'differential IK with joint limits'],
        ['rate', '100 Hz (physics 500 Hz)'],
        ['grasp', 'weld on close, < 2 cm'],
      ],
    },
    {
      id: 'dosing',
      title: 'Dosing',
      model: 'Closed loop',
      lines: [doseMode.toUpperCase(), `${flow.toFixed(3)} g/s`],
      status: seg.kind === 'dose' ? 'active' : 'ok',
      details: [
        ['phases', 'FAST > 0.55 g · SLOW > 0.06 g · PULSE'],
        ['feedback', `${FORMULATION_BALANCE.id} at 10 Hz, 100 ms lag`],
        ['prediction', 'in-flight mass = q̂ · (τ fall + τ scale)'],
        ['tolerance', 'max(0.010 g, 0.5 %)'],
      ],
    },
    {
      id: 'verification',
      title: 'Verification',
      model: 'Mass check',
      lines: [`${passed}/${R.ingredients.length} PASS`, 'tol ±0.010 g'],
      status: seg.kind === 'settle' || seg.kind === 'validate' || seg.kind === 'complete' ? 'active' : 'ok',
      details: [
        ['per ingredient', '|error| ≤ max(0.010 g, 0.5 %)'],
        ['batch', 'Σ ingredients vs recipe target'],
        ['evaluator', 'ground truth compared offline, never fed back'],
      ],
    },
  ]

  // ---- Run + summary ----------------------------------------------------
  const events = TL.events.filter((e) => e.time <= t).slice(-12)
  const finalMass = R.ingredients.reduce((acc, x) => acc + x.targetMass + x.doseError, 0)
  const validateSeg = TL.segments.find((s) => s.kind === 'validate')
  const summary = completed
    ? {
        targetMass: R.targetMass,
        finalMass,
        absoluteError: Math.abs(finalMass - R.targetMass),
        ingredientsDone: R.ingredients.length,
        ingredientsTotal: R.ingredients.length,
        recoveries,
        executionSeconds: validateSeg ? validateSeg.end : TL.duration,
        passed: Math.abs(finalMass - R.targetMass) <= Math.max(0.01, 0.005 * R.targetMass),
      }
    : null

  return {
    run: {
      id: DEMO_RUN_ID,
      status: completed ? 'completed' : 'running',
      mode: 'autonomous',
      elapsedSeconds: t,
      progress: t / TL.duration,
      phase: completed ? 'verify' : macroPhase(seg.kind, local),
      simulated: true,
    },
    recipe: { id: R.id, name: R.name, targetMass: R.targetMass, ingredients },
    execution: { currentStepId: seg.stepId, steps },
    balance: {
      id: FORMULATION_BALANCE.id,
      netMass: reading,
      totalMass: quantise(totalMass, 3),
      targetMass: balIng.targetMass,
      batchTargetMass: R.targetMass,
      flowRate: Math.max(0, flow),
      mode: doseMode,
      stable,
      ingredientId: balIdx !== null ? R.ingredients[balIdx].id : null,
      history,
      historyWindow: HISTORY_WINDOW,
    },
    robot: {
      fsmState: FSM[seg.kind],
      arm: ROBOT.arm,
      endEffector: seg.kind === 'dose' || seg.kind === 'settle' ? 'POUR' : gripper === 'open' ? 'GRIPPER' : 'GRIPPER + CONTAINER',
      targetObject: targetName,
      compound: ing && HANDLING.has(seg.kind) ? ing.compound : null,
      basePosition: basePos(quantise(baseX, 3)),
      eePosition: { x: quantise(ee.x, 3), y: quantise(ee.y, 3), z: quantise(ee.z, 3) },
      gripper,
      currentAction: action,
      tiltDeg: tilt,
      ikErrorMm: ikError,
      distanceToTarget: distToTarget,
      recoveries,
      replans: recoveries,
    },
    perception: {
      activeCamera: camera,
      detections,
      vessels: perceivedVessels,
      targetIndex: targetVessel ? targetVessel.index : null,
      target: targetName,
      targetClass: targetVessel ? targetVessel.cls : null,
      confidence: targetVessel ? targetVessel.confidence : null,
      barcode: barcodeKnown && ing ? ing.container.barcode : null,
      barcodeStatus,
      identity: ing && currentVerified && HANDLING.has(seg.kind) ? ing.compound : null,
      containerMl: ing && currentVerified && HANDLING.has(seg.kind) ? ing.container.ml : null,
      estimatedPosition: targetVessel && !targetVessel.stale ? targetVessel.position : null,
      localizationErrorMm: targetVessel && !targetVessel.stale ? vessel?.localizationErrorMm ?? LOCATE_ERROR_MM : null,
      targetBox: camera === 'wrist' && (seg.kind === 'barcode' || seg.kind === 'verify') ? { x: 0.3, y: 0.2, w: 0.4, h: 0.55 } : null,
      modules,
    },
    pipeline,
    events,
    summary,
    workcell: WORKCELL,
    evaluator: { groundTruth },
  }
}
