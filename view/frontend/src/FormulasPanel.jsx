// Every formula the operator has asked for in the chat, newest last: what was
// in it and what became of it — proposed and not sent yet, running as an order,
// finished, or rejected at the check with the reason the bench could not make
// it. The chat scrolls away; this does not.
import { Panel } from "./LabPanels";

const MARK = { proposed: "○", sent: "●", done: "✓", aborted: "■", rejected: "✗" };
const LABEL = { proposed: "Proposed", sent: "Running", done: "Done", aborted: "Stopped",
                rejected: "Rejected" };

const grams = (x) => (typeof x === "number" ? `${x.toFixed(x < 1 ? 3 : 2)} g` : "—");

function Row({ entry }) {
  const lines = entry.lines ?? [];
  return (
    <li className={`asked asked--${entry.status}`}>
      <span className="asked__mark">{MARK[entry.status] ?? "○"}</span>
      <span className="asked__name" title={entry.name}>
        {entry.name}
      </span>
      <span className="asked__lines" title={lines.map((l) => `${l.compound} ${grams(l.grams)}`).join(" · ")}>
        {lines.length ? lines.map((l) => `${l.compound} ${grams(l.grams)}`).join(" · ") : "—"}
      </span>
      <span className="asked__badge">
        {entry.order ? (
          <span className={`chip ${entry.status === "rejected" ? "chip--warn" : ""}`}>{entry.order}</span>
        ) : (
          <span className="asked__status">{LABEL[entry.status] ?? entry.status}</span>
        )}
      </span>
      {entry.problems?.length ? (
        <span className="asked__why">
          {entry.problems.map((p) => (p.compound === "—" ? p.reason : `${p.compound}: ${p.reason}`)).join(" · ")}
        </span>
      ) : null}
    </li>
  );
}

export default function FormulasPanel({ entries, style }) {
  const asked = entries ?? [];
  return (
    <Panel
      title="Formulas asked"
      right={<span className="chip">{asked.length || "none"}</span>}
      style={style}
      className="panel--asked"
    >
      {asked.length === 0 ? (
        <p className="asked__empty">Nothing asked yet. Type a formula in the chat and it is listed here.</p>
      ) : (
        <ol className="asked__list">
          {asked.map((entry) => (
            <Row key={entry.id} entry={entry} />
          ))}
        </ol>
      )}
    </Panel>
  );
}
