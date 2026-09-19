/**
 * Demo scenario, taken from the simulation.
 *
 * Geometry, balances, cameras and the seven loose containers are those of
 * `simulation/models/minihannover_scene.xml` (bench centred on the origin,
 * 6.0 × 1.5 m, worktop at z = 0.90 m, aisle at negative Y). Sample IDs and
 * EAN-13 codes are the real rows of `computer-vision/barcodes/lookup_table.json`.
 *
 * The scene has no robot yet. The demo assumes a Franka Panda on a linear rail
 * along the aisle edge of the bench, so one arm can serve the balances and the
 * containers spread along the 6 m worktop. Everything about it is in `ROBOT`;
 * a fixed base is a rail with one position and needs no UI change.
 */

import type { CameraId, Phase, Vec3, WorkcellState } from '../types'

export interface DemoContainer {
  id: string
  barcode: string
  ml: number
  lot: string
}

export interface DemoIngredient {
  id: string
  compound: string
  cas: string
  phase: Phase
  targetMass: number
  container: DemoContainer
  /** Index of the vessel on the bench that holds this compound. */
  vesselIndex: number
  /** Signed error of the final dose in grams; sums to +0.006 g over the batch. */
  doseError: number
}

export interface DemoRecipe {
  id: string
  name: string
  targetMass: number
  ingredients: DemoIngredient[]
}

export const DEMO_RUN_ID = 'RUN-042'

/**
 * A fougère base from the four aisle-side containers: two liquids in amber
 * flasks and two solids in HDPE powder bottles.
 */
export const DEMO_RECIPE: DemoRecipe = {
  id: 'FRG-031',
  name: 'Fougère Accord 01',
  targetMass: 10.0,
  ingredients: [
    {
      id: 'ing-linalool',
      compound: 'Linalool',
      cas: '78-70-6',
      phase: 'liquid',
      targetMass: 4.2,
      container: { id: 'SMP-0009', barcode: '2007063201700', ml: 50, lot: 'LOT-52639' },
      vesselIndex: 1,
      doseError: 0.004,
    },
    {
      id: 'ing-coumarin',
      compound: 'Coumarin',
      cas: '91-64-5',
      phase: 'powder',
      targetMass: 3.0,
      container: { id: 'PWD-0012', barcode: '2006117949254', ml: 250, lot: 'LOT-79591' },
      vesselIndex: 2,
      doseError: -0.003,
    },
    {
      id: 'ing-eugenol',
      compound: 'Eugenol',
      cas: '97-53-0',
      phase: 'liquid',
      targetMass: 1.0,
      container: { id: 'SMP-0021', barcode: '2001316174674', ml: 10, lot: 'LOT-16095' },
      vesselIndex: 3,
      doseError: 0.006,
    },
    {
      id: 'ing-menthol',
      compound: 'Menthol',
      cas: '2216-51-5',
      phase: 'powder',
      targetMass: 1.8,
      container: { id: 'PWD-0026', barcode: '2008565432623', ml: 100, lot: 'LOT-36337' },
      vesselIndex: 4,
      doseError: -0.001,
    },
  ],
}

export interface DemoVessel {
  index: number
  /** Free body in the scene that carries the container. */
  body: string
  sampleId: string
  cls: string
  ml: number
  /** Initial position in the scene (world frame, metres). */
  position: Vec3
  /** Offset of the perception estimate from the truth, a few millimetres. */
  estimateOffset: Vec3
  confidence: number
  localizationErrorMm: number
}

/** The seven free containers of `minihannover_scene.xml`, in scene order. */
export const VESSELS: DemoVessel[] = [
  { index: 1, body: 'loose_1', sampleId: 'SMP-0009', cls: 'amber bottle', ml: 50, position: { x: -2.25, y: -0.6, z: 0.9 }, estimateOffset: { x: 0.004, y: -0.007, z: 0 }, confidence: 0.91, localizationErrorMm: 11 },
  { index: 2, body: 'loose_2', sampleId: 'PWD-0012', cls: 'hdpe bottle', ml: 250, position: { x: -2.33, y: -0.46, z: 0.9 }, estimateOffset: { x: -0.006, y: 0.005, z: 0 }, confidence: 0.95, localizationErrorMm: 8 },
  { index: 3, body: 'loose_3', sampleId: 'SMP-0021', cls: 'amber bottle', ml: 10, position: { x: 0.72, y: -0.62, z: 0.9 }, estimateOffset: { x: 0.007, y: -0.008, z: 0 }, confidence: 0.84, localizationErrorMm: 14 },
  { index: 4, body: 'loose_4', sampleId: 'PWD-0026', cls: 'hdpe bottle', ml: 100, position: { x: 0.82, y: -0.5, z: 0.9 }, estimateOffset: { x: -0.005, y: 0.006, z: 0 }, confidence: 0.93, localizationErrorMm: 9 },
  { index: 5, body: 'loose_5', sampleId: 'SMP-0013', cls: 'amber bottle', ml: 30, position: { x: 0.1, y: 0.58, z: 0.9 }, estimateOffset: { x: 0.005, y: 0.009, z: 0 }, confidence: 0.88, localizationErrorMm: 12 },
  { index: 6, body: 'loose_6', sampleId: 'PWD-0008', cls: 'hdpe bottle', ml: 500, position: { x: 0.2, y: 0.45, z: 0.9 }, estimateOffset: { x: -0.008, y: -0.003, z: 0 }, confidence: 0.94, localizationErrorMm: 9 },
  { index: 7, body: 'loose_7', sampleId: 'SMP-0017', cls: 'amber bottle', ml: 20, position: { x: 1.95, y: 0.62, z: 0.9 }, estimateOffset: { x: 0.01, y: -0.004, z: 0 }, confidence: 0.86, localizationErrorMm: 13 },
]

/** Static workcell, as the simulation would send it in its snapshot. */
export const WORKCELL: WorkcellState = {
  bench: { x0: -3.0, x1: 3.0, y0: -0.75, y1: 0.75, top: 0.9 },
  balances: [
    { id: 'balance_1', position: { x: -1.85, y: -0.51, z: 0.904 }, active: false },
    { id: 'balance_2', position: { x: -0.2, y: -0.51, z: 0.9 }, active: true },
    { id: 'balance_3', position: { x: 1.3, y: -0.51, z: 0.9 }, active: false },
    { id: 'balance_4', position: { x: -1.0, y: 0.51, z: 0.9 }, active: false },
    { id: 'balance_5', position: { x: 0.75, y: 0.51, z: 0.904 }, active: false },
  ],
  rail: { x0: -2.8, x1: 2.8, y: -1.05 },
  cameras: [
    { id: 'overview', name: 'general', label: 'GENERAL', resolution: '1920×1080' },
    { id: 'robot', name: 'room_aisle', label: 'AISLE', resolution: '1280×720' },
    { id: 'wrist', name: 'wrist', label: 'WRIST', resolution: '1280×720' },
  ],
}

/** The demo robot: a Panda riding the rail; see the module comment. */
export const ROBOT = {
  arm: 'Franka Panda',
  /** Base height and lateral offset: the rail carriage at worktop height in the aisle. */
  baseY: -1.05,
  baseZ: 0.9,
  /** Rail position at the start of the run: in front of the formulation balance. */
  homeX: -0.2,
  /** Where the end effector rests while the carriage travels. */
  carry: { dy: 0.35, dz: 0.32 },
  reach: 0.85,
  /** Carriage speed along the rail, m/s. */
  railSpeed: 0.6,
}

/** Balance that holds the formulation vessel, and the pour pose above it. */
export const FORMULATION_BALANCE = WORKCELL.balances.find((b) => b.active) ?? WORKCELL.balances[1]
export const POUR_POSE: Vec3 = { x: FORMULATION_BALANCE.position.x, y: FORMULATION_BALANCE.position.y, z: 1.15 }

/**
 * The perturbation a judge would make: while the robot approaches the Eugenol
 * flask, the flask is moved. The robot must notice and replan.
 */
export const DISPLACEMENT = {
  vesselIndex: 3,
  to: { x: 0.58, y: -0.55, z: 0.9 } as Vec3,
}

export function vesselByIndex(index: number): DemoVessel {
  const v = VESSELS.find((x) => x.index === index)
  if (!v) throw new Error(`no demo vessel with index ${index}`)
  return v
}

export function cameraFor(id: CameraId) {
  return WORKCELL.cameras.find((c) => c.id === id) ?? WORKCELL.cameras[0]
}
