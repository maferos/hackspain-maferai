// The formula chat. A message goes to the backend (formula_chat.py), which
// answers and, for a formula, checks it against the flasks the live scan has
// named by their rings and shows it as the JSON the robot will receive. A
// formula can also be pasted or dropped as JSON. "Send to robot" makes it the
// order (workflow.py); from then on the robot narrates here what it crosses
// off, and the task panel follows it.
import { useEffect, useRef, useState } from "react";
import { Panel } from "./LabPanels";

const SUGGESTIONS = ["What's on the bench?", "2 g of FRG-101", "40 % geraniol, 60 % nerol, total 2 g"];
const HISTORY = 12;
const clock = (s) => `${String(Math.floor(s / 60)).padStart(2, "0")}:${String(Math.floor(s % 60)).padStart(2, "0")}`;
const JSON_EXAMPLE = '{"name": "My accord", "ingredients": [{"material": "Geraniol", "batch_g": 1.2}]}';

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

function Proposal({ formula, json, latest, busy, locked, scanning, onSend }) {
  const [showJson, setShowJson] = useState(false);
  const [copied, setCopied] = useState(false);
  const found = formula.ingredients.filter((i) => !i.problem);
  const text = json ? JSON.stringify(json, null, 2) : "";
  const copy = () =>
    navigator.clipboard?.writeText(text).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 1200);
    });
  return (
    <div className="proposal">
      <div className="proposal__title">
        <span>{formula.name}</span>
        <span className="proposal__tags">
          <span className="chip">{(formula.source ?? "chat").toUpperCase()}</span>
          {json ? (
            <button
              type="button"
              className={`chip-button ${showJson ? "chip-button--on" : ""}`}
              title="The formula as the robot receives it"
              onClick={() => setShowJson((v) => !v)}
            >
              {"{ }"}
            </button>
          ) : null}
        </span>
      </div>
      {showJson ? (
        <div className="proposal__json">
          <pre>{text}</pre>
          <button type="button" className="chip-button proposal__copy" onClick={copy}>
            {copied ? "copied" : "copy"}
          </button>
        </div>
      ) : (
        <ol className="proposal__list">
          {formula.ingredients.map((i) => (
            <li key={i.id} className={`proposal-row ${i.problem ? "proposal-row--off" : ""}`} title={i.problem ?? i.sampleId}>
              <span className="proposal-row__name">{i.compound}</span>
              <span className="proposal-row__meta">{i.problem ?? i.sampleId}</span>
              <span className="proposal-row__mass">{i.grams.toFixed(3)} g</span>
            </li>
          ))}
        </ol>
      )}
      <div className="proposal__foot">
        <span className="mono">
          {formula.targetMass.toFixed(3)} g ·{" "}
          {scanning ? "bench still being read" : `${found.length}/${formula.ingredients.length} on the bench`}
        </span>
        {latest && (scanning || found.length > 0) ? (
          <button
            type="button"
            className="chat-button chat-button--run"
            disabled={busy}
            onClick={onSend}
            title={
              scanning
                ? "Queue it: it is checked against the bench when the scan finishes"
                : locked
                  ? "Queue it behind the order the robot is on"
                  : "Make it the robot's order"
            }
          >
            {scanning || locked ? "Add to queue" : "Send to robot"}
          </button>
        ) : null}
      </div>
    </div>
  );
}

// `lab` is the LabState: the robot's narration comes from its order log, and
// the end of the scan from `scan.done`.
export default function FormulaChat({ backendUrl, lab, style, onAsked, onToast }) {
  const [messages, setMessages] = useState([]);
  const [draft, setDraft] = useState("");
  const [busy, setBusy] = useState(false);
  const [info, setInfo] = useState(null);
  const [dragging, setDragging] = useState(false);
  const logRef = useRef(null);
  const fileRef = useRef(null);
  const heard = useRef({ order: null, lines: 0, scanDone: null });
  const order = lab?.order ?? null;
  const running = order ? order.status === "running" : false;
  // The scan is the lab's first task; until it is done a formula can only be
  // queued, and it is matched to the bench when its turn comes.
  const scanning = lab?.scan ? !lab.scan.done : false;

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

  // The robot narrates: every new line of the order's log, and the end of the scan.
  const scanDone = lab?.scan?.done ?? null;
  const scanNamed = lab?.scan?.named ?? 0;
  useEffect(() => {
    const seen = heard.current;
    const lines = [];
    if (scanDone && seen.scanDone === false) {
      lines.push({ message: `Bench mapped: ${scanNamed} flasks named by their rings. Ready for a formula.`, level: "ok" });
    }
    seen.scanDone = scanDone;
    if (order) {
      if (order.id !== seen.order) {
        seen.order = order.id;
        seen.lines = 0;
      }
      lines.push(...order.log.slice(seen.lines));
      seen.lines = order.log.length;
    }
    if (lines.length) {
      setMessages((m) => [...m, ...lines.map((l) => ({ role: "robot", text: l.message, level: l.level, time: l.time }))]);
    }
  }, [order, scanDone, scanNamed]);

  useEffect(() => {
    logRef.current?.scrollTo({ top: logRef.current.scrollHeight, behavior: "smooth" });
  }, [messages, busy]);

  const say = (message) => setMessages((m) => [...m, message]);

  // What an answer means for the Formulas asked panel, and whether it is worth
  // interrupting the operator over. Only a rejection is: the reason is in the
  // chat, but they are probably watching the bench.
  const record = (answer, asked) => {
    const formula = answer.formula ?? answer.json ?? null;
    const lines = (formula?.ingredients ?? []).map((i) => ({
      compound: i.compound ?? i.material,
      grams: i.grams ?? i.batch_g,
    }));
    const name = formula?.name ?? (typeof asked === "string" ? asked : "Chat formula");
    if (answer.rejected) {
      onAsked?.({ name, lines, status: "rejected", order: answer.order, problems: answer.problems });
      const missing = (answer.problems ?? []).filter((p) => p.compound !== "—").map((p) => p.compound);
      onToast?.({
        level: "warn",
        title: `${answer.order ?? "The formula"} cannot run: the bench is short`,
        lines: (answer.problems ?? []).map((p) =>
          p.compound === "—" ? p.reason : `${p.compound} — ${p.reason}`),
        ask: missing.length
          ? `Restock ${missing.length < 3 ? missing.join(" and ")
              : `${missing.slice(0, -1).join(", ")} and ${missing[missing.length - 1]}`} and send it again.`
          : "Adjust the formula and send it again.",
      });
      return;
    }
    if (answer.order) {
      onAsked?.({ name, lines, status: "sent", order: answer.order });
    } else if (lines.length) {
      onAsked?.({ name, lines, status: "proposed" });
    }
  };

  const send = async (text) => {
    const message = text.trim();
    if (!message || busy) return;
    const history = messages
      .filter((m) => m.role !== "robot")
      .slice(-HISTORY)
      .map(({ role, text: t, formula }) => ({
        role,
        text: t,
        formula: formula ? { ingredients: formula.ingredients.map(({ compound, grams }) => ({ compound, grams })) } : undefined,
      }));
    const isJson = /^\s*[[{]/.test(message);
    say({ role: "user", text: isJson ? "JSON formula" : message, raw: isJson });
    setDraft("");
    setBusy(true);
    try {
      const answer = await post(`${backendUrl}/api/chat`, { message, history });
      say({ role: "assistant", text: answer.reply, formula: answer.action ? null : answer.formula,
            json: answer.json, error: answer.rejected });
      record(answer, message);
    } catch (error) {
      say({ role: "assistant", text: `Backend unreachable (${error.message}). Start view/backend/server.py.`, error: true });
    } finally {
      setBusy(false);
    }
  };

  const sendToRobot = async (formula) => {
    setBusy(true);
    try {
      const answer = await post(`${backendUrl}/api/formula`, { formula });
      say({ role: "assistant", text: answer.reply, error: answer.rejected });
      record({ ...answer, formula }, formula.name);
    } catch (error) {
      say({ role: "assistant", text: error.message, error: true });
    } finally {
      setBusy(false);
    }
  };

  const stop = async () => {
    try {
      const answer = await post(`${backendUrl}/api/formula/stop`);
      say({ role: "assistant", text: answer.reply });
    } catch (error) {
      say({ role: "assistant", text: error.message, error: true });
    }
  };

  const readFile = (file) => {
    if (file) file.text().then((text) => send(text));
  };

  const latest = messages.findLastIndex((m) => m.formula);
  const mode = info?.chat === "claude" ? "CLAUDE" : info ? "OFFLINE PARSER" : "OFFLINE";

  return (
    <Panel
      title="Formula"
      right={
        running ? (
          <button type="button" className="chat-button chat-button--stop" onClick={stop}>
            Stop {order.id}
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
      className={`panel--chat ${dragging ? "panel--drop" : ""}`}
    >
      <div
        className="chat__drop"
        onDragOver={(event) => {
          event.preventDefault();
          setDragging(true);
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={(event) => {
          event.preventDefault();
          setDragging(false);
          readFile(event.dataTransfer.files?.[0]);
        }}
      >
        <ol className="chat__log" ref={logRef}>
          {messages.length === 0 ? (
            <li className="chat__hint">
              Type a formula, or paste or drop its JSON. It is checked against the flasks the scan has named, then sent to the
              robot as an order.
              {info && !info.available ? " The bench scan is not running in this backend." : ""}
            </li>
          ) : null}
          {messages.map((m, i) =>
            m.role === "robot" ? (
              <li key={i} className={`chat-msg chat-msg--robot chat-msg--${m.level ?? "info"}`}>
                <span className="chat-msg__who">{typeof m.time === "number" ? clock(m.time) : "robot"}</span>
                {m.text}
              </li>
            ) : (
              <li key={i} className={`chat-msg chat-msg--${m.role} ${m.error ? "chat-msg--error" : ""}`}>
                {m.text ? <p className={`chat-msg__text ${m.raw ? "mono" : ""}`}>{m.text}</p> : null}
                {m.formula && m.formula.ingredients.length > 0 ? (
                  <Proposal
                    formula={m.formula}
                    json={m.json}
                    latest={i === latest}
                    busy={busy}
                    locked={running}
                    scanning={scanning}
                    onSend={() => sendToRobot(m.formula)}
                  />
                ) : null}
              </li>
            ),
          )}
          {busy ? <li className="chat-msg chat-msg--assistant chat-msg--pending">…</li> : null}
        </ol>
        {messages.length === 0 ? (
          <div className="chat__suggestions">
            {SUGGESTIONS.map((s) => (
              <button key={s} type="button" className="view-toggle" onClick={() => send(s)}>
                {s}
              </button>
            ))}
            <button type="button" className="view-toggle" title={JSON_EXAMPLE} onClick={() => setDraft(JSON_EXAMPLE)}>
              JSON example
            </button>
          </div>
        ) : null}
        <form
          className="chat__composer"
          onSubmit={(event) => {
            event.preventDefault();
            send(draft);
          }}
        >
          <textarea
            className="chat__input"
            rows={1}
            value={draft}
            onChange={(event) => setDraft(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === "Enter" && !event.shiftKey) {
                event.preventDefault();
                send(draft);
              }
            }}
            placeholder={running ? "Type stop, or ask about the bench…" : "e.g. 1.2 g geraniol, 0.5 g nerol, or paste JSON"}
            aria-label="Formula message"
          />
          <input
            ref={fileRef}
            type="file"
            accept=".json,application/json"
            hidden
            onChange={(event) => {
              readFile(event.target.files?.[0]);
              event.target.value = "";
            }}
          />
          <button
            type="button"
            className="chat-button chat-button--ghost"
            title="Load a formula JSON file"
            onClick={() => fileRef.current?.click()}
          >
            {"{ }"}
          </button>
          <button type="submit" className="chat-button" disabled={busy || !draft.trim()}>
            Send
          </button>
        </form>
      </div>
    </Panel>
  );
}
