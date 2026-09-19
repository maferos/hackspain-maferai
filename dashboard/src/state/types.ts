/**
 * Application state of the console.
 *
 * Every panel renders from a `LabState`. The state is produced by a
 * `LabStateSource` (see `sources/`): the demo source computes it from a
 * deterministic timeline, the live source assembles it from messages sent by
 * the simulation. Components never know which one is behind the state.
 *
 * Frames: everything is in the simulation's world frame, metres. The
 * minihannover bench is centred on the origin, 6.0 m along X and 1.5 m along
 * Y, worktop at z = 0.90 m. The aisle is at negative Y.
 *
 * Perception fields hold what the robot *perceives* (camera, detector,
 * barcode reader). Simulator ground truth, when present, lives only under
 * `evaluator` and is labelled as such wherever it is drawn.
 *
 * The Python side of this contract is `dashboard/bridge/labbridge/state.py`.
 */

export interface Vec3 {
  x: number
  y: number
  z: number
}

/** Axis-aligned box in normalised image coordinates (0..1). */
export interface Box2 {
  x: number
  y: number
  w: number
  h: number
}

export type RunStatus = 'idle' | 'running' | 'completed' | 'failed'
export type RunMode = 'autonomous' | 'manual'

/** Coarse phase shown in the header: PERCEIVE → IDENTIFY → PLAN → MOVE → DOSE → VERIFY. */
export type MacroPhase = 'perceive' | 'identify' | 'plan' | 'move' | 'dose' | 'verify'

export type StepStatus = 'queued' | 'active' | 'completed' | 'retrying' | 'failed'
export type IngredientStatus = 'queued' | 'active' | 'completed' | 'failed'
export type Phase = 'liquid' | 'powder'
export type DosingMode = 'fast' | 'slow' | 'pulse' | 'stopped'
export type CameraId = 'overview' | 'robot' | 'wrist'
export type ModuleStatus = 'idle' | 'active' | 'ok' | 'warn' | 'error'
export type GripperState = 'open' | 'closing' | 'attached' | 'releasing'
export type EventLevel = 'info' | 'ok' | 'warn' | 'error'
export type BarcodeStatus = 'idle' | 'reading' | 'verified' | 'mismatch'

export interface RunInfo {
  id: string
  status: RunStatus
  mode: RunMode
  /** Seconds since the run started. Frozen once the run completes. */
  elapsedSeconds: number
  /** 0..1 overall completion. */
  progress: number
  phase: MacroPhase | null
  /** True when the workcell is a simulator rather than hardware. */
  simulated: boolean
}

export interface Ingredient {
  id: string
  compound: string
  cas: string | null
  phase: Phase
  targetMass: number
  /** Mass attributed to this ingredient by the balance, null until dosing starts. */
  dispensedMass: number | null
  /** Sample ID of the container, known only after its barcode is verified. */
  containerId: string | null
  containerMl: number | null
  status: IngredientStatus
}

export interface Recipe {
  id: string
  name: string
  targetMass: number
  ingredients: Ingredient[]
}

export interface ExecutionStep {
  id: string
  label: string
  /** Ingredient this step belongs to, or null for recipe-level steps. */
  ingredientId: string | null
  status: StepStatus
  attempt: number
  startedAt: number | null
  completedAt: number | null
  /** Extra key/value lines shown when the step is active or retrying. */
  detail: Array<[string, string]>
}

export interface ExecutionState {
  currentStepId: string | null
  steps: ExecutionStep[]
}

export interface MassSample {
  time: number
  mass: number
}

export interface BalanceState {
  /** Which balance of the workcell holds the formulation vessel. */
  id: string | null
  /** Net mass since the last tare, i.e. the ingredient being dosed. */
  netMass: number
  /** Total formulation mass in the vessel. */
  totalMass: number
  /** Target for the ingredient being dosed. */
  targetMass: number
  batchTargetMass: number
  flowRate: number
  mode: DosingMode
  stable: boolean
  ingredientId: string | null
  /** Recent net-mass samples for the chart, oldest first. */
  history: MassSample[]
  /** Length of the history window in seconds. */
  historyWindow: number
}

export interface RobotState {
  fsmState: string
  arm: string
  endEffector: string
  targetObject: string | null
  compound: string | null
  /** Where the arm base is; changes when the arm rides the rail. */
  basePosition: Vec3
  eePosition: Vec3
  gripper: GripperState
  currentAction: string
  tiltDeg: number
  ikErrorMm: number
  distanceToTarget: number | null
  recoveries: number
  replans: number
}

export interface PerceivedVessel {
  /** Detection index, stable across frames for the demo. */
  index: number
  /** Sample ID once the barcode has been read, otherwise null. */
  id: string | null
  /** Detector class, e.g. "amber bottle" or "hdpe bottle". */
  cls: string
  confidence: number
  /** Position estimated from the camera and the bench plane. */
  position: Vec3
  /** True when the estimate is older than the last scene change. */
  stale: boolean
}

export interface PerceptionModules {
  detector: ModuleStatus
  localizer: ModuleStatus
  barcode: ModuleStatus
  wristCam: ModuleStatus
}

export interface PerceptionState {
  activeCamera: CameraId
  detections: number
  vessels: PerceivedVessel[]
  targetIndex: number | null
  target: string | null
  targetClass: string | null
  confidence: number | null
  barcode: string | null
  barcodeStatus: BarcodeStatus
  identity: string | null
  containerMl: number | null
  estimatedPosition: Vec3 | null
  localizationErrorMm: number | null
  /** Box of the target in the active camera image, when the camera sees it. */
  targetBox: Box2 | null
  modules: PerceptionModules
}

export interface PipelineNodeState {
  id: string
  title: string
  /** Model or method name, e.g. "YOLO11s". */
  model: string
  /** Two or three short lines of live values. */
  lines: string[]
  status: ModuleStatus
  /** Technical details shown when the node is expanded. */
  details: Array<[string, string]>
}

export interface LabEvent {
  id: string
  time: number
  message: string
  level: EventLevel
}

export interface CompletionSummary {
  targetMass: number
  finalMass: number
  absoluteError: number
  ingredientsDone: number
  ingredientsTotal: number
  recoveries: number
  executionSeconds: number
  passed: boolean
}

/** Worktop extent in the world frame, metres. */
export interface WorkcellBench {
  x0: number
  x1: number
  y0: number
  y1: number
  top: number
}

export interface WorkcellBalance {
  /** Body name in the scene, e.g. "balance_2". */
  id: string
  position: Vec3
  /** True for the balance that holds the formulation vessel. */
  active: boolean
}

/** Linear axis the arm base rides along the bench, if any. */
export interface WorkcellRail {
  x0: number
  x1: number
  y: number
}

export interface WorkcellCamera {
  id: CameraId
  /** Camera name in the scene, e.g. "general" or "wrist". */
  name: string
  label: string
  resolution: string
}

/** Static description of the workcell, sent once in the snapshot. */
export interface WorkcellState {
  bench: WorkcellBench
  balances: WorkcellBalance[]
  rail: WorkcellRail | null
  cameras: WorkcellCamera[]
}

/** Ground-truth object pose from the simulator. Evaluation only. */
export interface GroundTruthVessel {
  index: number
  /** Body name in the scene, e.g. "loose_3". */
  body: string
  position: Vec3
  /** Tilt of the container in degrees, non-zero while pouring. */
  tiltDeg: number
}

/**
 * Object poses read from the simulator for evaluation and for the schematic
 * workcell drawing. Never fed to the planner; never shown as perception.
 */
export interface EvaluatorState {
  groundTruth: GroundTruthVessel[]
}

export interface LabState {
  run: RunInfo
  recipe: Recipe
  execution: ExecutionState
  balance: BalanceState
  robot: RobotState
  perception: PerceptionState
  pipeline: PipelineNodeState[]
  events: LabEvent[]
  summary: CompletionSummary | null
  workcell: WorkcellState
  evaluator: EvaluatorState | null
}

/** Recursive partial used by live `state_update` patches. */
export type DeepPartial<T> = T extends (infer U)[]
  ? U[]
  : T extends object
    ? { [K in keyof T]?: DeepPartial<T[K]> }
    : T
