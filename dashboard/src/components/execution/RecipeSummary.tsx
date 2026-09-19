import type { Recipe } from '../../state/types'
import { fmtMass } from '../../lib/format'
import { IngredientRow } from './IngredientRow'

/** Active recipe: name, batch target and one row per ingredient. */
export function RecipeSummary({ recipe }: { recipe: Recipe }) {
  const done = recipe.ingredients.filter((i) => i.status === 'completed').length
  return (
    <div className="shrink-0 border-b border-line px-2.5 pb-2 pt-2">
      <div className="flex items-baseline justify-between gap-2">
        <div className="min-w-0">
          <div className="truncate text-[1rem] font-semibold text-fg">{recipe.name}</div>
          <div className="num text-[0.68rem] tracking-[0.1em] text-muted">
            {recipe.id} · {recipe.ingredients.length} ingredients
          </div>
        </div>
        <div className="text-right">
          <div className="text-[0.62rem] uppercase tracking-[0.14em] text-muted">Batch target</div>
          <div className="num text-[1rem] text-fg">{fmtMass(recipe.targetMass)} g</div>
        </div>
      </div>
      <div className="mt-1.5 grid grid-cols-[1fr_5rem_5rem_1.25rem] gap-2 pl-2 pr-1 text-[0.6rem] uppercase tracking-[0.12em] text-muted">
        <span>Compound · container</span>
        <span className="text-right">Target</span>
        <span className="text-right">Actual</span>
        <span className="text-center">{done}/{recipe.ingredients.length}</span>
      </div>
      <div className="mt-0.5 flex flex-col">
        {recipe.ingredients.map((ing) => (
          <IngredientRow key={ing.id} ingredient={ing} />
        ))}
      </div>
    </div>
  )
}
