// The balance, one of the three panels in the dock under the viewport. It says
// one thing — what the pan reads right now — so it is the narrow one of the
// three. Its top edge lights while the pipeline's dosing module is active.

const g = (x, digits = 3) => (typeof x === "number" ? x.toFixed(digits) : "—");

export function Panel({ title, right, children, footer, live, className, style }) {
  return (
    <section className={`panel ${live ? "panel--live" : ""} ${className ?? ""}`} style={style}>
      <header className="panel__header">
        <span>{title}</span>
        {right}
      </header>
      <div className="panel__body">{children}</div>
      {footer ? <footer className="panel__footer">{footer}</footer> : null}
    </section>
  );
}

const moduleActive = (state, id) => state.pipeline?.find((n) => n.id === id)?.status === "active";

export default function BalancePanel({ state, connected, style }) {
  if (!state || state.run.status === "idle") {
    return (
      <Panel title="Balance" style={style} className="panel--balance">
        <div className="balance__readout balance__readout--off">
          <span className={`status-dot ${connected ? "status-dot--live" : "status-dot--off"}`} />
          <span>{connected ? "Waiting…" : "Offline"}</span>
        </div>
      </Panel>
    );
  }
  const b = state.balance;
  return (
    <Panel
      title="Balance"
      right={<span className="chip">{b.id ?? "—"}</span>}
      live={moduleActive(state, "dosing")}
      style={style}
      className="panel--balance"
    >
      <div className="balance__readout">
        <div className="big">
          {g(b.netMass)}
          <small>g</small>
        </div>
      </div>
    </Panel>
  );
}
