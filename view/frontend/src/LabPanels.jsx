// Two small panels under the viewport, fed by the LabState: what the robot is
// doing and what the balance reads. A panel lights its top edge while its
// module of the pipeline is active (motion for the robot, dosing for the
// balance).

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

function Row({ label, value }) {
  return (
    <div className="kv">
      <span>{label}</span>
      <span>{value}</span>
    </div>
  );
}

const moduleActive = (state, id) => state.pipeline?.find((n) => n.id === id)?.status === "active";

// The rail the arm rides, with the balances along it and the carriage where the
// robot base is now.
function RailTrack({ state }) {
  const rail = state.workcell?.rail;
  const x = state.robot.basePosition?.x;
  if (!rail || typeof x !== "number") return <Row label="Base x" value={`${g(x, 2)} m`} />;
  const pct = (v) => `${Math.min(100, Math.max(0, ((v - rail.x0) / (rail.x1 - rail.x0)) * 100))}%`;
  return (
    <div className="rail">
      <Row label="Rail" value={`${g(x, 2)} m`} />
      <div className="rail__track">
        {(state.workcell.balances ?? []).map((b) => (
          <span
            key={b.id}
            className={`rail__balance ${b.active ? "rail__balance--active" : ""}`}
            style={{ left: pct(b.position.x) }}
            title={b.active ? `${b.id} · formulation vessel` : b.id}
          />
        ))}
        <span className="rail__carriage" style={{ left: pct(x) }} />
      </div>
    </div>
  );
}

function RobotPanel({ state }) {
  const r = state.robot;
  const p = state.perception;
  return (
    <Panel
      title="Robot"
      right={<span className="chip">{r.fsmState}</span>}
      footer={r.currentAction}
      live={moduleActive(state, "motion")}
    >
      <Row label="Target" value={r.targetObject ?? "—"} />
      <Row label="Compound" value={r.compound ?? "—"} />
      <Row label={p.barcodeStatus === "ring" ? "Ring" : "Barcode"} value={p.barcode ?? "—"} />
      <Row label="Gripper" value={`${r.gripper.toUpperCase()} · tilt ${g(r.tiltDeg, 1)}°`} />
      <RailTrack state={state} />
    </Panel>
  );
}

// Mass samples arrive only while dosing, so the last run of samples without a
// gap is the current (or the last) dose.
const SAMPLE_GAP_S = 1.5;

function lastDose(history) {
  let i = history.length - 1;
  while (i > 0 && history[i].time - history[i - 1].time <= SAMPLE_GAP_S) i--;
  return history.slice(i);
}

// Net mass of the current dose rising towards the target (dashed). Between
// doses the last curve stays, dimmed, without a target.
function MassTrace({ balance, live }) {
  const points = lastDose(balance.history ?? []);
  if (points.length < 2) return <div className="trace trace--empty" />;
  const t0 = points[0].time;
  const t1 = Math.max(t0 + 8, points[points.length - 1].time);
  const top = Math.max(live ? balance.targetMass : 0, ...points.map((s) => s.mass), 0.001) * 1.15;
  const x = (t) => (((t - t0) / (t1 - t0)) * 100).toFixed(2);
  const y = (m) => (40 - (Math.max(0, m) / top) * 40).toFixed(2);
  const line = points.map((s) => `${x(s.time)},${y(s.mass)}`).join(" ");
  const area = `M${x(t0)},40 L${line.replaceAll(" ", " L")} L${x(points[points.length - 1].time)},40 Z`;
  return (
    <svg
      className={`trace ${live ? "" : "trace--past"}`}
      viewBox="0 0 100 40"
      preserveAspectRatio="none"
      role="img"
      aria-label={live ? "Net mass of the current dose" : "Net mass of the last dose"}
    >
      <path className="trace__area" d={area} />
      {live && balance.targetMass > 0 ? (
        <line className="trace__target" x1="0" x2="100" y1={y(balance.targetMass)} y2={y(balance.targetMass)} />
      ) : null}
      <polyline className="trace__line" points={line} />
    </svg>
  );
}

function BalancePanel({ state }) {
  const b = state.balance;
  const dosing = moduleActive(state, "dosing");
  return (
    <Panel title="Balance" right={<span className="chip">{b.id ?? "—"}</span>} live={dosing} className="panel--balance">
      <div className="balance__readout">
        <div className="big">
          {g(b.netMass)}
          <small>g</small>
        </div>
        <MassTrace balance={b} live={dosing} />
      </div>
      <div className="kv-grid">
        <Row label="Target" value={`${g(b.targetMass)} g`} />
        <Row label="Mode" value={b.mode.toUpperCase()} />
        <Row label="Flow" value={`${g(b.flowRate)} g/s`} />
        <Row label="Stable" value={b.stable ? "YES" : "NO"} />
      </div>
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
        <span>{connected ? "Waiting for the scan to start…" : "Lab state offline"}</span>
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
