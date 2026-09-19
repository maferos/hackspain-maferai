import { Check } from 'lucide-react'
import type { Ingredient } from '../../state/types'
import { cn, fmtMass } from '../../lib/format'

/** One recipe line: compound, container, requested and dispensed mass, status. */
export function IngredientRow({ ingredient }: { ingredient: Ingredient }) {
  const { status } = ingredient
  return (
    <div
      className={cn(
        'grid grid-cols-[1fr_5rem_5rem_1.25rem] items-center gap-2 border-l-2 py-1 pl-2 pr-1 leading-tight',
        status === 'active' ? 'border-active bg-active/8' : status === 'completed' ? 'border-ok/60' : 'border-transparent',
      )}
    >
      <div className="min-w-0">
        <div className={cn('truncate text-[0.86rem]', status === 'queued' ? 'text-fg-2' : 'text-fg')}>{ingredient.compound}</div>
        <div className="num text-[0.66rem] tracking-[0.08em] text-muted">
          {ingredient.containerId ?? 'container —'}
          {ingredient.containerMl ? ` · ${ingredient.containerMl} mL` : ''}
          {` · ${ingredient.phase}`}
        </div>
      </div>
      <div className="num text-right text-[0.82rem] text-fg-2">{fmtMass(ingredient.targetMass)} g</div>
      <div className={cn('num text-right text-[0.82rem]', status === 'active' ? 'text-active' : status === 'completed' ? 'text-fg' : 'text-muted')}>
        {ingredient.dispensedMass === null ? '—' : `${fmtMass(ingredient.dispensedMass)} g`}
      </div>
      <div className="flex justify-center">
        {status === 'completed' ? (
          <Check size={13} className="text-ok" />
        ) : status === 'active' ? (
          <span className="size-2 rounded-full bg-active animate-pulse-dot" />
        ) : status === 'failed' ? (
          <span className="size-2 rounded-full bg-err" />
        ) : (
          <span className="size-2 rounded-full border border-queued" />
        )}
      </div>
    </div>
  )
}
