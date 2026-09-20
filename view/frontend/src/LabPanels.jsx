// The balance, one of the three panels in the dock under the viewport. It shows
// the pan up close — the vessel the mixture is dosed into, and the balance's own
// display — so the reading is watched where it happens instead of as a bare
// number. Its top edge lights while the pipeline's dosing module is active.

const g = (x, digits = 3) => (typeof x === "number" ? x.toFixed(digits) : "—");
const signed = (x, digits = 3) => `${x >= 0 ? "+" : "−"}${Math.abs(x).toFixed(digits)}`;
const clamp01 = (x) => (Number.isFinite(x) ? Math.min(1, Math.max(0, x)) : 0);

// What the balance is doing, in the words its own display would use. The
// scripted run dials the valve (fast/slow/pulse); the live backend only says
// whether it is dosing. Anything else is shown as it comes.
const MODE = { fast: "FAST", slow: "SLOW", pulse: "PULSE", dosing: "DOSING", stopped: "IDLE" };

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

// The last `windowS` seconds of mass samples, mapped into the display's little
// box. The samples arrive as their own `mass_sample` messages, so this is the
// reading's real history, not a redraw of netMass.
function trace(history, windowS, box) {
  const pts = (history ?? []).filter((s) => typeof s.mass === "number" && typeof s.time === "number");
  if (pts.length < 2) return null;
  const last = pts[pts.length - 1].time;
  const win = pts.filter((s) => s.time >= last - (windowS > 0 ? windowS : 30));
  if (win.length < 2) return null;
  const t0 = win[0].time;
  const span = last - t0 || 1;
  let lo = Math.min(...win.map((s) => s.mass));
  let hi = Math.max(...win.map((s) => s.mass));
  if (hi - lo < 1e-6) {
    lo -= 0.5;
    hi += 0.5;
  }
  const at = (s) => [
    box.x + ((s.time - t0) / span) * box.w,
    box.y + box.h - ((s.mass - lo) / (hi - lo)) * box.h,
  ];
  const line = win.map((s) => at(s).map((n) => n.toFixed(1)).join(",")).join(" ");
  const [x0] = at(win[0]);
  const [x1] = at(win[win.length - 1]);
  const bottom = box.y + box.h;
  return { line, area: `${x0.toFixed(1)},${bottom} ${line} ${x1.toFixed(1)},${bottom}` };
}

// The pan seen close: the vessel the mixture goes into, and the display under
// it. Every number and every level comes from the balance state; the chrome
// around them is just chrome.
function BalanceCloseUp({ b }) {
  const filled = clamp01(b.batchTargetMass > 0 ? b.totalMass / b.batchTargetMass : 0);
  const liquid = 40 * filled;
  const spark = trace(b.history, b.historyWindow, { x: 170, y: 108, w: 50, h: 32 });
  const dosing = b.mode && b.mode !== "stopped";

  return (
    <svg className="balance-closeup" viewBox="0 0 240 176" preserveAspectRatio="xMidYMid meet" role="img"
      aria-label={`Balance reading ${g(b.netMass)} grams`}>
      <title>{`${g(b.totalMass)} g of ${g(b.batchTargetMass)} g in the vessel`}</title>
      <defs>
        <linearGradient id="bal-pan" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#5f6061" />
          <stop offset="1" stopColor="#323233" />
        </linearGradient>
        <linearGradient id="bal-liquid" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#90aacc" stopOpacity="0.95" />
          <stop offset="1" stopColor="#426693" stopOpacity="0.8" />
        </linearGradient>
        <linearGradient id="bal-spark" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#426693" stopOpacity="0.3" />
          <stop offset="1" stopColor="#426693" stopOpacity="0" />
        </linearGradient>
        <clipPath id="bal-glass">
          <path d="M104 16 L108 60 L132 60 L136 16 Z" />
        </clipPath>
      </defs>

      {/* the draft shield behind the pan */}
      <rect x="34" y="2" width="172" height="56" rx="6" className="balance-closeup__shield" />
      <line x1="70" y1="4" x2="70" y2="56" className="balance-closeup__glint" />

      {/* the vessel the mixture is dosed into: the level is totalMass of batchTargetMass */}
      <rect x="103" y={60 - liquid} width="34" height={liquid} fill="url(#bal-liquid)" clipPath="url(#bal-glass)" />
      <path d="M104 16 L108 60 L132 60 L136 16" className="balance-closeup__glass" />
      <ellipse cx="120" cy="16" rx="16" ry="3.4" className="balance-closeup__rim" />
      {dosing && <line x1="120" y1="4" x2="120" y2="18" className="balance-closeup__pour" />}

      {/* the pan */}
      <ellipse cx="120" cy="69" rx="64" ry="13" className="balance-closeup__pan-edge" />
      <ellipse cx="120" cy="66" rx="64" ry="13" fill="url(#bal-pan)" className="balance-closeup__pan" />

      {/* the balance's own display */}
      <rect x="6" y="78" width="228" height="94" rx="8" className="balance-closeup__bezel" />
      <rect x="13" y="85" width="214" height="80" rx="5" className="balance-closeup__lcd" />

      <text x="22" y="101" className={`balance-lcd__flag ${b.stable ? "" : "balance-lcd__flag--wobbly"}`}>
        {b.stable ? "ST" : "~"}
      </text>
      <text x="218" y="101" textAnchor="end" className="balance-lcd__mode">
        {MODE[b.mode] ?? (b.mode ?? "").toUpperCase()}
        {b.flowRate > 0 ? `  ${g(b.flowRate)} g/s` : ""}
      </text>

      <text x="148" y="138" textAnchor="end"
        className={`balance-lcd__value ${b.stable ? "" : "balance-lcd__value--wobbly"}`}>
        {g(b.netMass)}
      </text>
      <text x="154" y="138" className="balance-lcd__unit">g</text>

      {spark && (
        <>
          <polygon points={spark.area} fill="url(#bal-spark)" />
          <polyline points={spark.line} className="balance-lcd__trace" />
        </>
      )}

      <text x="22" y="158" className="balance-lcd__row">
        {b.targetMass > 0 ? `target ${g(b.targetMass)} g` : "no target"}
      </text>
      {b.targetMass > 0 && (
        <text x="218" y="158" textAnchor="end" className="balance-lcd__row">
          {`\u0394 ${signed(b.netMass - b.targetMass)}`}
        </text>
      )}
    </svg>
  );
}

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
  const ingredient = state.recipe?.ingredients?.find((i) => i.id === b.ingredientId);
  return (
    <Panel
      title="Balance"
      right={<span className="chip">{b.id ?? "—"}</span>}
      live={moduleActive(state, "dosing")}
      style={style}
      className="panel--balance"
      footer={
        <span className="balance__caption">
          <span>{ingredient ? ingredient.compound : "\u2014"}</span>
          <span className="balance__caption-batch">mix {g(b.totalMass)} / {g(b.batchTargetMass)} g</span>
        </span>
      }
    >
      <div className="balance__closeup">
        <BalanceCloseUp b={b} />
      </div>
    </Panel>
  );
}
