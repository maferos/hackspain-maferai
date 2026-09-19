// The autonomy pipeline as a chain of modules, from the camera at the top to
// the mass check at the bottom, each lit by its status in the LabState. The
// footer shows the latest event.
import { Panel } from "./LabPanels";

const STATUS = { idle: "idle", active: "working", ok: "ready", warn: "warning", error: "error" };

const clock = (s) =>
  `${String(Math.floor(s / 60)).padStart(2, "0")}:${String(Math.floor(s % 60)).padStart(2, "0")}`;

function Summary({ nodes }) {
  const warnings = nodes.filter((n) => n.status === "warn" || n.status === "error").length;
  if (warnings > 0) return <span className="chip chip--warn">{warnings === 1 ? "1 warning" : `${warnings} warnings`}</span>;
  const working = nodes.find((n) => n.status === "active");
  return <span className="chip">{working ? working.title : "Ready"}</span>;
}

function LastEvent({ events }) {
  const last = events?.[events.length - 1];
  if (!last) return null;
  return (
    <span className={`event event--${last.level ?? "info"}`} title={last.message}>
      <span className="event__time">{clock(last.time)}</span> {last.message}
    </span>
  );
}

export default function PipelinePanel({ state, connected, style }) {
  if (!state || state.run.status === "idle") {
    return (
      <Panel title="Pipeline" style={style} className="panel--pipeline">
        <p className="pipeline__empty">{connected ? "Waiting for lab state…" : "Lab state offline"}</p>
      </Panel>
    );
  }
  const nodes = state.pipeline ?? [];
  const running = state.run.status === "running";
  return (
    <Panel
      title="Pipeline"
      right={<Summary nodes={nodes} />}
      footer={<LastEvent events={state.events} />}
      style={style}
      className="panel--pipeline"
    >
      <ol className={`chain ${running ? "chain--running" : ""}`}>
        {nodes.map((n) => (
          <li
            key={n.id}
            className={`chain__node chain__node--${n.status}`}
            title={`${n.title} (${n.model}): ${STATUS[n.status] ?? n.status}\n${n.lines.join(" · ")}`}
          >
            <span className="chain__dot" />
            <span className="chain__title">{n.title}</span>
            <span className="chain__metric">{n.lines[0]}</span>
          </li>
        ))}
      </ol>
    </Panel>
  );
}
