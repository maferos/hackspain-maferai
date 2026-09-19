import type { CompletionSummary } from '../../state/types'
import { fmtClock, fmtMass } from '../../lib/format'

/** Compact completion card over the viewport; the simulation stays visible. */
export function CompletionBanner({ summary }: { summary: CompletionSummary }) {
  const rows: Array<[string, string]> = [
    ['Target mass', `${fmtMass(summary.targetMass)} g`],
    ['Final mass', `${fmtMass(summary.finalMass)} g`],
    ['Absolute error', `${fmtMass(summary.absoluteError)} g`],
    ['Ingredients', `${summary.ingredientsDone} / ${summary.ingredientsTotal}`],
    ['Recoveries', String(summary.recoveries)],
    ['Execution time', fmtClock(summary.executionSeconds)],
  ]
  return (
    <div className="absolute bottom-12 left-3 w-[21rem] border border-ok/50 bg-panel/92 backdrop-blur-sm">
      <div className="flex items-center justify-between border-b border-ok/40 px-3 py-1.5">
        <span className="text-[0.8rem] font-semibold tracking-[0.18em] text-ok">FORMULATION COMPLETE</span>
        <span className="num text-[0.7rem] tracking-[0.14em] text-ok">{summary.passed ? 'PASS' : 'FAIL'}</span>
      </div>
      <dl className="grid grid-cols-[auto_1fr] gap-x-4 px-3 py-2 text-[0.78rem] leading-[1.35rem]">
        {rows.map(([k, v]) => (
          <div key={k} className="contents">
            <dt className="text-muted">{k}</dt>
            <dd className="num text-right text-fg">{v}</dd>
          </div>
        ))}
      </dl>
    </div>
  )
}
