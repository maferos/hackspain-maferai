// The formula the robot has in hand, driven by the LabState. At the top, where
// it is in its workflow (scan → formula → check → fetch → done); then the order, one row
// per ingredient with its steps as dots, or the bench scan's tally before the
// first order; and below, the plan around the current step (a few done and
// crossed off, the active one, the next ones), grouped by ingredient.
//
// It shares the dock under the viewport with the balance and the pipeline, so
// everything below the header scrolls as one: the box is a few hundred pixels
// tall and the plan alone can outgrow it.
//
// Without a backend the viewer plays the recorded scripted run, which has no
// workflow or order: the formula checklist shows it as before.

const KEEP_DONE = 4;
const SHOW_NEXT = 3;
const DONE = new Set(["completed", "failed", "skipped"]);
const STEP_NAMES = { locate: "Locate", pick: "Pick", carry: "Carry", dose: "Dose", verify: "Verify", return: "Return" };

const g = (x, digits = 3) => (typeof x === "number" ? x.toFixed(digits) : "—");
const signed = (x, digits = 3) => `${x < 0 ? "−" : "+"}${Math.abs(x).toFixed(digits)}`;

const fmtClock = (seconds) => {
  const s = Math.max(0, Math.floor(seconds ?? 0));
  return `${String(Math.floor(s / 60)).padStart(2, "0")}:${String(s % 60).padStart(2, "0")}`;
};

// The whole workflow as a row of stages.
function WorkflowBar({ stages }) {
  return (
    <ol className="stages" aria-label="Workflow">
      {stages.map((stage) => (
        <li key={stage.id} className={`stage stage--${stage.status}`} title={`${stage.label}: ${stage.status}`}>
          <span className="stage__mark">{stage.status === "completed" ? "✓" : stage.status === "failed" ? "✗" : ""}</span>
          <span className="stage__label">{stage.label}</span>
        </li>
      ))}
    </ol>
  );
}

// What the live scan has found so far.
function ScanSummary({ scan }) {
  return (
    <div className="formula">
      <div className="formula__title">
        <span>Bench scan</span>
        <span className={`chip ${scan.error ? "chip--warn" : ""}`}>{scan.error ? "ERROR" : scan.done ? "MAPPED" : "SCANNING"}</span>
      </div>
      <div className="scan-tally">
        <span>
          <strong>{scan.named}</strong>/{scan.tracked} named by their ring
        </span>
        <span className="mono">
          {scan.waiting} to look at · {scan.empty} not samples · {scan.unreachable} out of reach
        </span>
      </div>
      {scan.error ? <div className="formula__summary formula__summary--fail">{scan.error}</div> : null}
    </div>
  );
}

function ingredientStatus(ing) {
  if (ing.problem) return "skipped";
  if (ing.steps.some((s) => s.status === "failed")) return "failed";
  if (ing.steps.every((s) => DONE.has(s.status))) return "completed";
  return ing.steps.some((s) => s.status !== "queued") ? "active" : "queued";
}

// The order: one row per ingredient, its steps as dots.
function OrderCard({ order }) {
  const current = (ing) => ing.steps.find((s) => s.status === "active");
  const remaining = Math.max(0, order.estimateSeconds - order.elapsedSeconds);
  const qc = order.qc;
  return (
    <div className="formula">
      <div className="formula__title">
        <span title={order.formula.name}>{order.formula.name}</span>
        <span className="chip" title={`from the ${order.source}, run by the ${order.executor} executor`}>
          {order.id}
        </span>
      </div>
      <ol className="order__list">
        {order.ingredients.map((ing) => {
          const status = ingredientStatus(ing);
          const step = current(ing);
          const dose = ing.steps.find((s) => s.id === "dose");
          const weighing = ing.mass !== null && dose && dose.status === "active";
          return (
            <li key={ing.id} className={`order-row order-row--${status}`}>
              <span className="formula-row__check">
                {status === "completed" ? "✓" : status === "failed" ? "✗" : status === "active" ? "●" : "○"}
              </span>
              <span className="order-row__name">
                {ing.compound}
                <span className="formula-row__meta"> {ing.sampleId ?? ""}</span>
              </span>
              <span className="order-row__mass">
                {ing.mass !== null ? (
                  <>
                    {g(ing.mass)} {weighing ? `/ ${g(ing.grams)} g` : <span className="formula-row__delta">{signed(ing.mass - ing.grams)}</span>}
                  </>
                ) : (
                  `${g(ing.grams)} g`
                )}
              </span>
              <span className="order-row__steps">
                {ing.steps.map((s) => (
                  <span
                    key={s.id}
                    className={`dot dot--${s.status}`}
                    title={`${STEP_NAMES[s.id] ?? s.id}: ${s.status}${s.note ? ` · ${s.note}` : ""}`}
                  />
                ))}
              </span>
              <span className="order-row__note">
                {ing.problem ?? (step ? `${STEP_NAMES[step.id] ?? step.id}${step.note ? ` · ${step.note}` : "…"}` : status === "queued" ? "queued" : "")}
              </span>
              {weighing ? (
                <span className="formula-row__bar">
                  <span style={{ width: `${Math.min(1, ing.mass / ing.grams) * 100}%` }} />
                </span>
              ) : null}
            </li>
          );
        })}
      </ol>
      {qc ? (
        <div className={`formula__summary ${qc.passed ? "formula__summary--pass" : "formula__summary--fail"}`}>
          <span>{qc.passed ? `✓ ${order.id} complete` : `✗ ${order.id} finished with problems`}</span>
          <span className="mono">
            {qc.finalMass !== null ? `${g(qc.finalMass)} / ${g(qc.targetMass)} g · ` : ""}
            {fmtClock(qc.seconds)}
            {qc.note ? ` · ${qc.note}` : ""}
          </span>
        </div>
      ) : (
        <div className="formula__total">
          <span>
            {order.status === "aborted" ? "Stopped" : `${order.done}/${order.total} done`}
          </span>
          <span className="mono">
            {order.status === "queued" ? "waiting for the arm" : `${fmtClock(order.elapsedSeconds)} · ETA ~${fmtClock(remaining)}`}
          </span>
        </div>
      )}
    </div>
  );
}

// The recorded scripted run, when no backend is running.
function FormulaChecklist({ state }) {
  const { recipe, balance, summary } = state;
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
                {ing.status === "completed" && dispensed !== null ? (
                  <>
                    {g(dispensed)} g <span className="formula-row__delta">{signed(dispensed - ing.targetMass)}</span>
                  </>
                ) : ing.status === "active" && dispensed !== null ? (
                  `${g(dispensed)} / ${g(ing.targetMass)} g`
                ) : (
                  `${g(ing.targetMass)} g`
                )}
              </span>
              {ing.status === "active" ? (
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
            {done}/{recipe.ingredients.length} added
          </span>
          <span className="mono">
            {g(balance.totalMass)} / {g(recipe.targetMass)} g
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
  const detail = step.detail
    .map(([k, v]) => `${k} ${v}`.trim())
    .filter(Boolean)
    .join(" · ");
  switch (step.status) {
    case "completed":
      return `Done · ${fmtClock(step.completedAt)}${detail ? ` · ${detail}` : ""}`;
    case "skipped":
      return `Skipped${detail ? ` · ${detail}` : ""}`;
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
  const pivot = current === -1 ? steps.findIndex((s) => s.status === "queued") : current;
  const cut = pivot === -1 ? steps.length : pivot;
  const doneBefore = steps.slice(0, cut).filter((s) => DONE.has(s.status));
  const hidden = Math.max(0, doneBefore.length - KEEP_DONE);
  const next = steps.slice(cut + (current === -1 ? 0 : 1)).filter((s) => s.status === "queued").slice(0, SHOW_NEXT);
  const visible = [...doneBefore.slice(hidden), ...(current === -1 ? [] : [steps[current]]), ...next];

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
          <h2>Current formula</h2>
          <span className={`status-dot ${connected ? "status-dot--live" : "status-dot--off"}`} />
        </header>
        <ol className="task-list">
          <li className="task-item task-item--empty">{connected ? "Waiting for the scan to start…" : "Lab state offline"}</li>
        </ol>
      </aside>
    );
  }
  const { run } = state;
  return (
    <aside className="task-panel">
      <header className="task-panel__header">
        <div className="task-panel__title">
          <h2>Current formula</h2>
          <span className="task-panel__run">
            {run.id} · {run.status.toUpperCase()} · {fmtClock(run.elapsedSeconds)}
            {run.status === "running" && run.progress > 0 ? ` · ${Math.round(run.progress * 100)} %` : ""}
          </span>
        </div>
        <div className="task-panel__badges">
          {run.scripted ? (
            <span className="chip chip--warn" title="A recorded run: no backend is publishing the lab state">
              SCRIPTED
            </span>
          ) : null}
          <span className={`status-dot ${connected ? "status-dot--live" : "status-dot--off"}`} />
        </div>
      </header>
      <div className="task-panel__scroll">
        {state.workflow ? <WorkflowBar stages={state.workflow.stages} /> : null}
        {state.order ? (
          <OrderCard order={state.order} />
        ) : state.scan ? (
          <ScanSummary scan={state.scan} />
        ) : (
          <FormulaChecklist state={state} />
        )}
        <PlanList state={state} />
      </div>
    </aside>
  );
}
