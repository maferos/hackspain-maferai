// The formula chat. A message goes to the backend (formula_chat.py), which
// answers and, for a formula, checks it against the flasks the live scan has
// named by their rings; Pick has the arm fetch them (scan_state.py), and the
// task panel follows it.
import { useEffect, useRef, useState } from "react";
import { Panel } from "./LabPanels";

const SUGGESTIONS = ["What's on the bench?", "2 g of FRG-101", "40 % geraniol, 60 % nerol, total 2 g"];
const HISTORY = 12;

const clock = (s) => (s >= 60 ? `${Math.floor(s / 60)} min ${String(Math.round(s % 60)).padStart(2, "0")} s` : `${Math.round(s)} s`);

async function post(url, body) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body ?? {}),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.detail ?? `HTTP ${res.status}`);
  return data;
}

function Proposal({ formula, latest, running, busy, onRun }) {
  const picks = formula.estimate.picks;
  const ok = formula.ingredients.filter((i) => !i.problem);
  return (
    <div className="proposal">
      <div className="proposal__title">
        <span>{formula.name}</span>
        {formula.id !== "CHAT" ? <span className="chip">{formula.id}</span> : null}
      </div>
      <ol className="proposal__list">
        {formula.ingredients.map((i) => (
          <li key={i.id} className={`proposal-row ${i.problem ? "proposal-row--off" : ""}`} title={i.problem ?? i.sampleId}>
            <span className="proposal-row__name">{i.compound}</span>
            <span className="proposal-row__meta">{i.problem ?? i.sampleId}</span>
            <span className="proposal-row__mass">{i.grams.toFixed(3)} g</span>
          </li>
        ))}
      </ol>
      <div className="proposal__foot">
        <span className="mono">
          {formula.targetMass.toFixed(3)} g · {picks} flask{picks === 1 ? "" : "s"} · ~{clock(formula.estimate.seconds)}
        </span>
        {latest && ok.length > 0 ? (
          <button
            type="button"
            className="chat-button chat-button--run"
            disabled={running || busy}
            onClick={onRun}
            title="The arm picks each flask and puts it back: it carries a gripper, not the pipette"
          >
            Pick
          </button>
        ) : null}
      </div>
    </div>
  );
}

// `fetching`: the arm is picking a formula's flasks.
export default function FormulaChat({ backendUrl, fetching, style }) {
  const [messages, setMessages] = useState([]);
  const [draft, setDraft] = useState("");
  const [busy, setBusy] = useState(false);
  const [info, setInfo] = useState(null);
  const logRef = useRef(null);
  const running = fetching;

  useEffect(() => {
    let cancelled = false;
    let timer;
    const poll = () =>
      fetch(`${backendUrl}/api/formulation`)
        .then((res) => res.json())
        .then((data) => !cancelled && setInfo(data))
        .catch(() => !cancelled && setInfo(null))
        .finally(() => {
          if (!cancelled) timer = setTimeout(poll, 5000);
        });
    poll();
    return () => {
      cancelled = true;
      clearTimeout(timer);
    };
  }, [backendUrl]);

  useEffect(() => {
    logRef.current?.scrollTo({ top: logRef.current.scrollHeight, behavior: "smooth" });
  }, [messages, busy]);

  const say = (message) => setMessages((m) => [...m, message]);

  const send = async (text) => {
    const message = text.trim();
    if (!message || busy) return;
    const history = messages.slice(-HISTORY).map(({ role, text: t, formula }) => ({
      role,
      text: t,
      formula: formula ? { ingredients: formula.ingredients.map(({ compound, grams }) => ({ compound, grams })) } : undefined,
    }));
    say({ role: "user", text: message });
    setDraft("");
    setBusy(true);
    try {
      const answer = await post(`${backendUrl}/api/chat`, { message, history });
      say({ role: "assistant", text: answer.reply, formula: answer.action ? null : answer.formula });
    } catch (error) {
      say({ role: "assistant", text: `Backend unreachable (${error.message}). Start view/backend/server.py.`, error: true });
    } finally {
      setBusy(false);
    }
  };

  const start = async (formula) => {
    setBusy(true);
    try {
      const answer = await post(`${backendUrl}/api/formulation/start`, { formula });
      say({ role: "assistant", text: answer.reply });
    } catch (error) {
      say({ role: "assistant", text: error.message, error: true });
    } finally {
      setBusy(false);
    }
  };

  const stop = async () => {
    try {
      await post(`${backendUrl}/api/formulation/stop`);
      say({ role: "assistant", text: "Stopped; the arm finishes what it is holding and goes back to watching." });
    } catch (error) {
      say({ role: "assistant", text: error.message, error: true });
    }
  };

  const latest = messages.findLastIndex((m) => m.formula);
  const mode = info?.chat === "claude" ? "CLAUDE" : info ? "OFFLINE PARSER" : "OFFLINE";

  return (
    <Panel
      title="Formula"
      right={
        running ? (
          <button type="button" className="chat-button chat-button--stop" onClick={stop}>
            Stop
          </button>
        ) : (
          <span
            className={`chip ${info ? "" : "chip--warn"}`}
            title={
              info?.chat === "claude"
                ? "Claude reads free-form requests"
                : info
                  ? "Set ANTHROPIC_API_KEY on the backend for free-form requests"
                  : "Backend not reachable"
            }
          >
            {mode}
          </span>
        )
      }
      style={style}
      className="panel--chat"
    >
      <ol className="chat__log" ref={logRef}>
        {messages.length === 0 ? (
          <li className="chat__hint">
            Type a formula: it is checked against the flasks the scan has named, and the arm can fetch them.
            {info && !info.available ? " The bench scan is not running in this backend." : ""}
          </li>
        ) : null}
        {messages.map((m, i) => (
          <li key={i} className={`chat-msg chat-msg--${m.role} ${m.error ? "chat-msg--error" : ""}`}>
            {m.text ? <p className="chat-msg__text">{m.text}</p> : null}
            {m.formula && m.formula.ingredients.length > 0 ? (
              <Proposal formula={m.formula} latest={i === latest} running={running} busy={busy} onRun={() => start(m.formula)} />
            ) : null}
          </li>
        ))}
        {busy ? <li className="chat-msg chat-msg--assistant chat-msg--pending">…</li> : null}
      </ol>
      {messages.length === 0 ? (
        <div className="chat__suggestions">
          {SUGGESTIONS.map((s) => (
            <button key={s} type="button" className="view-toggle" onClick={() => send(s)}>
              {s}
            </button>
          ))}
        </div>
      ) : null}
      <form
        className="chat__composer"
        onSubmit={(event) => {
          event.preventDefault();
          send(draft);
        }}
      >
        <input
          className="chat__input"
          value={draft}
          onChange={(event) => setDraft(event.target.value)}
          placeholder={running ? "Type stop…" : "e.g. 1.2 g geraniol, 0.5 g nerol"}
          aria-label="Formula message"
        />
        <button type="submit" className="chat-button" disabled={busy || !draft.trim()}>
          Send
        </button>
      </form>
    </Panel>
  );
}
