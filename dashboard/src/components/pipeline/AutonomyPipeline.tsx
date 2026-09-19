import { Fragment, useEffect, useState } from 'react'
import { ChevronRight } from 'lucide-react'
import { useLabState } from '../../state/LabStateProvider'
import { Panel } from '../ui/Panel'
import { PipelineNode } from './PipelineNode'

/** Horizontal chain of the autonomy modules, highlighting the ones in use. */
export function AutonomyPipeline() {
  const { state } = useLabState()
  const [expanded, setExpanded] = useState<string | null>(null)

  useEffect(() => {
    if (!expanded) return
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') setExpanded(null)
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [expanded])

  const right = <span className="text-[0.62rem] uppercase tracking-[0.12em] text-muted">click a module for details</span>

  return (
    <Panel title="Autonomy pipeline" right={right} bodyClassName="flex items-stretch gap-1 px-2 py-1.5">
      {state.pipeline.map((node, i) => (
        <Fragment key={node.id}>
          {i > 0 ? (
            <span className="flex shrink-0 items-center text-muted/70">
              <ChevronRight size={14} />
            </span>
          ) : null}
          <PipelineNode node={node} expanded={expanded === node.id} onToggle={() => setExpanded(expanded === node.id ? null : node.id)} />
        </Fragment>
      ))}
    </Panel>
  )
}
