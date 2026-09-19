// Task panel driven by the LabState: at the top the bench scan's tally, or the
// formula (crossed off as each ingredient is added, or fetched), and below it
// the plan around the current step (a few done, the active one, the next
// ones), grouped by the step's group or ingredient.

const KEEP_DONE = 4;
const SHOW_NEXT = 3;

const g = (x, digits = 3) => (typeof x === "number" ? x.toFixed(digits) : "—");
const signed = (x, digits = 3) => `${x < 0 ? "−" : "+"}${Math.abs(x).toFixed(digits)}`;

const fmtClock = (seconds) => {
  const s = Math.max(0, Math.floor(seconds ?? 0));
  return `${String(Math.floor(s / 60)).padStart(2, "0")}:${String(s % 60).padStart(2, "0")}`;
};

// What the live scan has found so far.
function ScanSummary({ scan }) {
  return (
    <div className="formula">
      <div className="formula__title">
        <span>Bench scan</span>
        <span className={`chip ${scan.error ? "chip--warn" : ""}`}>{scan.error ? "ERROR" : scan.done ? "MAPPED" : "SCANNING"}</span>
      </div>
      <div className="scan-tally">
        <div>
          <span className="big">{scan.named}</span>
          <small> / {scan.tracked} named by their ring</small>
        </div>
        <span className="mono">
          {scan.waiting} to look at · {scan.empty} not samples · {scan.unreachable} out of reach
        </span>
      </div>
      {scan.error ? <div className="formula__summary formula__summary--fail">{scan.error}</div> : null}
    </div>
  );
}

function FormulaChecklist({ state }) {
  const { recipe, balance, summary } = state;
  const fetch = recipe.mode === "fetch";
  const done = recipe.ingredients.filter((i) => i.status === "completed").length;
  return (
    <div className="formula">
      <div className="formula__title">
        <span>{recipe.name}</span>
        <span className="chip">{recipe.id}</span>
      </div>
      <ol className="formula__list">
        {recipe.ingredients.map((ing) => {
          const dispensed = ing.dispensedMass;
          const progress = dispensed !== null && ing.targetMass > 0 ? Math.min(1, dispensed / ing.targetMass) : 0;
          return (
            <li key={ing.id} className={`formula-row formula-row--${ing.status}`}>
              <span className="formula-row__check">{ing.status === "completed" ? "✓" : ing.status === "active" ? "●" : "○"}</span>
              <span className="formula-row__name">
                {ing.compound}
                {ing.containerId ? <span className="formula-row__meta"> {ing.containerId}</span> : null}
              </span>
              <span className="formula-row__mass">
                {fetch ? (
                  `${g(ing.targetMass)} g`
                ) : ing.status === "completed" && dispensed !== null ? (
                  <>
                    {g(dispensed)} g <span className="formula-row__delta">{signed(dispensed - ing.targetMass)}</span>
                  </>
                ) : ing.status === "active" && dispensed !== null ? (
                  `${g(dispensed)} / ${g(ing.targetMass)} g`
                ) : (
                  `${g(ing.targetMass)} g`
                )}
              </span>
              {fetch && ing.note ? <span className="formula-row__note">{ing.note}</span> : null}
              {ing.status === "active" && !fetch ? (
                <span className="formula-row__bar">
                  <span style={{ width: `${progress * 100}%` }} />
                </span>
              ) : null}
            </li>
          );
        })}
      </ol>
      {summary ? (
        <div className={`formula__summary ${summary.passed ? "formula__summary--pass" : "formula__summary--fail"}`}>
          <span>{summary.passed ? "✓ Formulation complete · PASS" : "✗ Formulation out of tolerance"}</span>
          <span className="mono">
            {g(summary.finalMass)} g · error {g(summary.absoluteError)} g · {summary.recoveries} recovery · {fmtClock(summary.executionSeconds)}
          </span>
        </div>
      ) : (
        <div className="formula__total">
          <span>
            {done}/{recipe.ingredients.length} {fetch ? "fetched" : "added"}
          </span>
          <span className="mono">
            {fetch ? `${g(recipe.targetMass)} g formula · not dosed` : `${g(balance.totalMass)} / ${g(recipe.targetMass)} g`}
          </span>
        </div>
      )}
    </div>
  );
}

function groupTitle(step, steps, recipe) {
  if (step.group) return step.group;
  if (step.ingredientId) {
    const ing = recipe.ingredients.find((i) => i.id === step.ingredientId);
    return ing ? `${ing.compound} · ${g(ing.targetMass)} g` : step.ingredientId;
  }
  const firstIngredientStep = steps.findIndex((s) => s.ingredientId);
  return steps.indexOf(step) < firstIngredientStep ? "Setup" : "Final check";
}

function stepMeta(step, now) {
  const detail = step.detail.map(([k, v]) => `${k} ${v}`).join(" · ");
  switch (step.status) {
    case "completed":
      return `Done · ${fmtClock(step.completedAt)}`;
    case "retrying":
      return `Retrying · ${step.detail.map(([, v]) => v).join(" · ")}`;
    case "active":
      return `In progress · ${fmtClock(step.startedAt ?? now)}${detail ? ` · ${detail}` : ""}`;
    case "failed":
      return `Failed${detail ? ` · ${detail}` : ""}`;
    default:
      return "Next";
  }
}

function PlanList({ state }) {
  const { steps } = state.execution;
  const current = steps.findIndex((s) => s.status === "active" || s.status === "retrying");
  const pivot = current === -1 ? steps.length : current;
  const doneBefore = steps.slice(0, pivot).filter((s) => s.status === "completed");
  const hidden = Math.max(0, doneBefore.length - KEEP_DONE);
  const visible = [...doneBefore.slice(hidden), ...(current === -1 ? [] : [steps[current]]), ...steps.slice(pivot + 1).filter((s) => s.status === "queued").slice(0, SHOW_NEXT)];

  const rows = [];
  let lastGroup;
  for (const step of visible) {
    const group = groupTitle(step, steps, state.recipe);
    if (group !== lastGroup) {
      rows.push(
        <li key={`group-${step.id}`} className="plan-group">
          {group}
        </li>,
      );
      lastGroup = group;
    }
    const status = step.status === "completed" ? "done" : step.status;
    rows.push(
      <li key={step.id} className={`task-item task-item--${status}`}>
        <span className="task-item__marker" />
        <div className="task-item__body">
          <p className="task-item__label">{step.label}</p>
          <p className="task-item__meta">{stepMeta(step, state.run.elapsedSeconds)}</p>
        </div>
      </li>,
    );
  }

  return (
    <ol className="task-list">
      {hidden > 0 ? <li className="plan-earlier">+{hidden} earlier steps done</li> : null}
      {rows}
      {visible.length === 0 ? <li className="task-item task-item--empty">Waiting for tasks…</li> : null}
    </ol>
  );
}

export default function LabTaskPanel({ state, connected }) {
  if (!state || state.run.status === "idle") {
    return (
      <aside className="task-panel">
        <header className="task-panel__header">
          <h2>Robot tasks</h2>
          <span className={`status-dot ${connected ? "status-dot--live" : "status-dot--off"}`} />
        </header>
        <ol className="task-list">
          <li className="task-item task-item--empty">{connected ? "Waiting for the scan to start…" : "Lab state offline"}</li>
        </ol>
      </aside>
    );
  }
  const { run } = state;
  const scanOnly = state.scan && state.recipe.ingredients.length === 0;
  return (
    <aside className="task-panel">
      <header className="task-panel__header">
        <div className="task-panel__title">
          <h2>Robot tasks</h2>
          <span className="task-panel__run">
            {run.id} · {run.status.toUpperCase()} · {fmtClock(run.elapsedSeconds)}
          </span>
        </div>
        <div className="task-panel__badges">
          {run.scripted ? (
            <span className="chip chip--warn" title="The sequence is scripted; the real planner is not connected yet">
              SCRIPTED
            </span>
          ) : null}
          <span className={`status-dot ${connected ? "status-dot--live" : "status-dot--off"}`} />
        </div>
      </header>
      {scanOnly ? <ScanSummary scan={state.scan} /> : <FormulaChecklist state={state} />}
      <PlanList state={state} />
    </aside>
  );
}
