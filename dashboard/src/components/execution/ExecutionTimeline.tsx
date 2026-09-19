import { Fragment, useEffect, useRef } from 'react'
import { Check, RefreshCw, X } from 'lucide-react'
import type { ExecutionStep, Recipe } from '../../state/types'
import { cn, fmtClock, fmtMass } from '../../lib/format'

interface ExecutionTimelineProps {
  steps: ExecutionStep[]
  currentStepId: string | null
  recipe: Recipe
}

function StepIcon({ status }: { status: ExecutionStep['status'] }) {
  switch (status) {
    case 'completed':
      return <Check size={12} className="text-ok" />
    case 'active':
      return <span className="size-2 rounded-full bg-active animate-pulse-dot" />
    case 'retrying':
      return <RefreshCw size={12} className="animate-spin text-warn [animation-duration:2s]" />
    case 'failed':
      return <X size={12} className="text-err" />
    default:
      return <span className="size-2 rounded-full border border-queued" />
  }
}

/** Vertical checklist of the autonomous plan, following the active step. */
export function ExecutionTimeline({ steps, currentStepId, recipe }: ExecutionTimelineProps) {
  const listRef = useRef<HTMLOListElement | null>(null)
  const activeRef = useRef<HTMLLIElement | null>(null)

  useEffect(() => {
    const list = listRef.current
    const row = activeRef.current
    if (!list || !row) return
    const top = row.offsetTop - list.clientHeight * 0.38 + row.clientHeight / 2
    list.scrollTo({ top: Math.max(0, top), behavior: 'smooth' })
  }, [currentStepId])

  let lastGroup: string | null | undefined

  return (
    <ol ref={listRef} className="scroll-thin relative min-h-0 flex-1 overflow-y-auto px-1.5 py-1.5">
      {steps.map((step) => {
        const group = step.ingredientId
        const showHeader = group !== lastGroup
        lastGroup = group
        const ingredient = group ? recipe.ingredients.find((i) => i.id === group) : null
        const active = step.status === 'active' || step.status === 'retrying'
        return (
          <Fragment key={step.id}>
            {showHeader && ingredient ? (
              <li className="mt-1.5 flex items-center gap-2 px-1 pb-0.5 text-[0.6rem] uppercase tracking-[0.14em] text-muted">
                <span className="h-px flex-1 bg-line" />
                <span>
                  {ingredient.compound} · {fmtMass(ingredient.targetMass)} g
                </span>
                <span className="h-px flex-1 bg-line" />
              </li>
            ) : null}
            <li
              ref={active ? activeRef : null}
              className={cn(
                'flex flex-col border-l-2 px-2 py-[0.18rem] transition-colors',
                step.status === 'active' && 'border-active bg-active/10',
                step.status === 'retrying' && 'border-warn bg-warn/10',
                step.status === 'failed' && 'border-err bg-err/10',
                step.status === 'completed' && 'border-transparent',
                step.status === 'queued' && 'border-transparent',
              )}
            >
              <div className="flex items-center gap-2 leading-[1.3rem]">
                <span className="flex w-3.5 shrink-0 items-center justify-center">
                  <StepIcon status={step.status} />
                </span>
                <span
                  className={cn(
                    'min-w-0 flex-1 truncate text-[0.84rem]',
                    step.status === 'completed' && 'text-fg-2/80',
                    step.status === 'active' && 'font-medium text-fg',
                    step.status === 'retrying' && 'font-medium text-warn',
                    step.status === 'failed' && 'text-err',
                    step.status === 'queued' && 'text-muted',
                  )}
                >
                  {step.label}
                </span>
                {step.status === 'completed' && step.completedAt !== null ? <span className="num text-[0.66rem] text-muted">{fmtClock(step.completedAt)}</span> : null}
                {step.status === 'retrying' ? <span className="num text-[0.66rem] tracking-[0.1em] text-warn">RETRYING</span> : null}
              </div>
              {active && step.detail.length ? (
                <dl className="num ml-5.5 mt-0.5 grid grid-cols-[auto_1fr] gap-x-3 gap-y-0 text-[0.72rem] leading-[1.15rem]">
                  {step.detail.map(([k, v]) => (
                    <div key={k} className="contents">
                      <dt className="uppercase tracking-[0.1em] text-muted">{k}</dt>
                      <dd className={cn(step.status === 'retrying' ? 'text-warn' : 'text-active')}>{v}</dd>
                    </div>
                  ))}
                </dl>
              ) : null}
            </li>
          </Fragment>
        )
      })}
    </ol>
  )
}
