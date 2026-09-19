import { useLabState } from '../../state/LabStateProvider'
import { Panel } from '../ui/Panel'
import { RecipeSummary } from './RecipeSummary'
import { ExecutionTimeline } from './ExecutionTimeline'

/** Recipe plus the live autonomous plan. */
export function ExecutionPanel() {
  const { state } = useLabState()
  const { recipe, execution } = state
  const done = execution.steps.filter((s) => s.status === 'completed').length
  const right = (
    <span className="num text-[0.7rem] tracking-[0.1em] text-muted">
      {done}/{execution.steps.length} steps
    </span>
  )
  return (
    <Panel title="Formulation execution" right={right} bodyClassName="flex flex-col">
      <RecipeSummary recipe={recipe} />
      <ExecutionTimeline steps={execution.steps} currentStepId={execution.currentStepId} recipe={recipe} />
    </Panel>
  )
}
