// Two small panels under the viewport, fed by the LabState: what the robot is
// doing and what the balance reads.

const g = (x, digits = 3) => (typeof x === "number" ? x.toFixed(digits) : "—");

function Panel({ title, right, children, footer }) {
  return (
    <section className="panel">
      <header className="panel__header">
        <span>{title}</span>
        {right}
      </header>
      <div className="panel__body">{children}</div>
      {footer ? <footer className="panel__footer">{footer}</footer> : null}
    </section>
  );
}

function Row({ label, value }) {
  return (
    <div className="kv">
      <span>{label}</span>
      <span>{value}</span>
    </div>
  );
}

function RobotPanel({ state }) {
  const r = state.robot;
  const p = state.perception;
  return (
    <Panel title="Robot" right={<span className="chip">{r.fsmState}</span>} footer={r.currentAction}>
      <Row label="Target" value={r.targetObject ?? "—"} />
      <Row label="Compound" value={r.compound ?? "—"} />
      <Row label="Barcode" value={p.barcode ?? "—"} />
      <Row label="Gripper" value={r.gripper.toUpperCase()} />
      <Row label="Base x" value={`${g(r.basePosition?.x, 2)} m`} />
      <Row label="Tilt" value={`${g(r.tiltDeg, 1)}°`} />
    </Panel>
  );
}

function BalancePanel({ state }) {
  const b = state.balance;
  const progress = b.targetMass > 0 ? Math.min(1, Math.max(0, b.netMass / b.targetMass)) : 0;
  return (
    <Panel title="Balance" right={<span className="chip">{b.id ?? "—"}</span>}>
      <div className="big">
        {g(b.netMass)}
        <small>g</small>
      </div>
      <div className="bar">
        <div style={{ width: `${progress * 100}%` }} />
      </div>
      <Row label="Target" value={`${g(b.targetMass)} g`} />
      <Row label="Mode" value={b.mode.toUpperCase()} />
      <Row label="Flow" value={`${g(b.flowRate)} g/s`} />
      <Row label="Stable" value={b.stable ? "YES" : "NO"} />
    </Panel>
  );
}

// `show` picks which of the two panels are open, `robotShare` is the Robot
// panel's fraction of the width and `divider` the handle drawn between them.
export default function LabPanels({ state, connected, show, style, robotShare, divider }) {
  if (!state || state.run.status === "idle") {
    return (
      <div className="panels panels--empty">
        <span className={`status-dot ${connected ? "status-dot--live" : "status-dot--off"}`} />
        <span>{connected ? "Waiting for lab state…" : "Lab state offline"}</span>
      </div>
    );
  }
  const both = show.robot && show.balance;
  const columns = both ? `${robotShare}fr 1rem ${1 - robotShare}fr` : "1fr";
  return (
    <div className="panels" style={{ ...style, gridTemplateColumns: columns }}>
      {show.robot && <RobotPanel state={state} />}
      {both && divider}
      {show.balance && <BalancePanel state={state} />}
    </div>
  );
}
