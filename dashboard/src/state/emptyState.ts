/**
 * Blank state used before the live source has received its first snapshot.
 * Every panel renders from it without special cases.
 */

import type { LabState, PipelineNodeState } from './types'

const NODES: Array<[string, string, string]> = [
  ['camera', 'Camera', '—'],
  ['detection', 'Object detection', '—'],
  ['localization', '3D localization', '—'],
  ['barcode', 'Barcode ID', '—'],
  ['planner', 'Task planner', '—'],
  ['motion', 'Motion', '—'],
  ['dosing', 'Dosing', '—'],
  ['verification', 'Verification', '—'],
]

export function emptyState(runId = '—'): LabState {
  const pipeline: PipelineNodeState[] = NODES.map(([id, title, model]) => ({
    id,
    title,
    model,
    lines: ['waiting', '—'],
    status: 'idle',
    details: [],
  }))
  return {
    run: { id: runId, status: 'idle', mode: 'autonomous', elapsedSeconds: 0, progress: 0, phase: null, simulated: true },
    recipe: { id: '—', name: 'No recipe loaded', targetMass: 0, ingredients: [] },
    execution: { currentStepId: null, steps: [] },
    balance: {
      id: null,
      netMass: 0,
      totalMass: 0,
      targetMass: 0,
      batchTargetMass: 0,
      flowRate: 0,
      mode: 'stopped',
      stable: true,
      ingredientId: null,
      history: [],
      historyWindow: 30,
    },
    robot: {
      fsmState: 'IDLE',
      arm: '—',
      endEffector: 'GRIPPER',
      targetObject: null,
      compound: null,
      basePosition: { x: 0, y: -1.05, z: 0.9 },
      eePosition: { x: 0, y: 0, z: 0 },
      gripper: 'open',
      currentAction: 'Waiting for state',
      tiltDeg: 0,
      ikErrorMm: 0,
      distanceToTarget: null,
      recoveries: 0,
      replans: 0,
    },
    perception: {
      activeCamera: 'overview',
      detections: 0,
      vessels: [],
      targetIndex: null,
      target: null,
      targetClass: null,
      confidence: null,
      barcode: null,
      barcodeStatus: 'idle',
      identity: null,
      containerMl: null,
      estimatedPosition: null,
      localizationErrorMm: null,
      targetBox: null,
      modules: { detector: 'idle', localizer: 'idle', barcode: 'idle', wristCam: 'idle' },
    },
    pipeline,
    events: [],
    summary: null,
    workcell: {
      bench: { x0: -3.0, x1: 3.0, y0: -0.75, y1: 0.75, top: 0.9 },
      balances: [],
      rail: null,
      cameras: [
        { id: 'overview', name: 'general', label: 'GENERAL', resolution: '1920×1080' },
        { id: 'robot', name: 'room_aisle', label: 'AISLE', resolution: '1280×720' },
        { id: 'wrist', name: 'wrist', label: 'WRIST', resolution: '1280×720' },
      ],
    },
    evaluator: null,
  }
}
