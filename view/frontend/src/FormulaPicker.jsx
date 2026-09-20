// The formulas the lab already knows, and the door the run comes in through.
//
// The bench scan is the lab's first task, but the lab waits to be asked: the
// backend only starts it once a formula has been sent (see `want_scan` in
// server.py). This panel is what asks. It lists harness/formulas, sends the one
// the operator picks to the existing POST /api/formula, and then collapses to a
// line, because the shelf is not what anyone watches once the arm is working.
//
// `loaded` comes from the backend rather than from a click, so a reload does not
// re-open the picker over a run that is already going, and a formula typed into
// the chat collapses it too — what closes it is the lab having a task at all.
import { useCallback, useEffect, useState } from "react";
import { Panel } from "./LabPanels";

// The offline parser's own default batch (formula_chat.DEFAULT_BATCH_G).
const DEFAULT_BATCH_G = 3;

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

export default function FormulaPicker({ backendUrl, onAsked, onToast }) {
  const [data, setData] = useState(null);
  const [batch, setBatch] = useState(DEFAULT_BATCH_G);
  const [busy, setBusy] = useState(null);
  const [reply, setReply] = useState(null);
  const [open, setOpen] = useState(false);

  const load = useCallback(
    () =>
      fetch(`${backendUrl}/api/formulas`)
        .then((res) => res.json())
        .then(setData)
        .catch(() => setData(null)),
    [backendUrl],
  );

  useEffect(() => {
    let cancelled = false;
    let timer;
    const poll = () =>
      fetch(`${backendUrl}/api/formulas`)
        .then((res) => res.json())
        .then((d) => !cancelled && setData(d))
        .catch(() => !cancelled && setData(null))
        .finally(() => {
          if (!cancelled) timer = setTimeout(poll, 5000);
        });
    poll();
    return () => {
      cancelled = true;
      clearTimeout(timer);
    };
  }, [backendUrl]);

  // The same entry the chat writes, so "Formulas asked" and the rejection toast
  // do not care which of the two sent the formula (see FormulaChat's `record`).
  const record = (answer, name) => {
    const lines = (answer.json?.ingredients ?? []).map((i) => ({
      compound: i.compound ?? i.material,
      grams: i.grams ?? i.batch_g,
    }));
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
    } else if (answer.order) {
      onAsked?.({ name, lines, status: "sent", order: answer.order });
    }
  };

  const send = async (formula) => {
    if (busy) return;
    setBusy(formula.id);
    try {
      const answer = await post(`${backendUrl}/api/formula`, { id: formula.id, batch_g: batch });
      setReply(answer.reply);
      record(answer, formula.name);
      setOpen(false);
      await load();
    } catch (error) {
      setReply(error.message);
      onToast?.({ level: "warn", title: "The formula did not reach the robot", lines: [error.message] });
    } finally {
      setBusy(null);
    }
  };

  if (data && data.available === false) return null;

  const loaded = data?.loaded ?? null;
  const ready = data?.ready ?? false;
  const formulas = data?.formulas ?? [];

  if (loaded && !open) {
    return (
      <Panel
        title="Lab formulas"
        className="panel--picker panel--picker-shut"
        right={
          <button type="button" className="view-toggle" onClick={() => setOpen(true)}>
            Pick another
          </button>
        }
      >
        <p className="picker__loaded">
          <span className="chip">{loaded.id}</span>
          <span className="picker__loaded-name" title={loaded.name}>{loaded.name}</span>
        </p>
        {reply ? <p className="picker__reply">{reply}</p> : null}
      </Panel>
    );
  }

  return (
    <Panel
      title="Lab formulas"
      className="panel--picker"
      right={
        <span className={`chip ${data ? "" : "chip--warn"}`} title="the formulas in harness/formulas">
          {data ? formulas.length : "offline"}
        </span>
      }
    >
      {data === null ? (
        <p className="picker__empty">Backend not reachable. Start view/backend/server.py.</p>
      ) : (
        <>
          <p className="picker__lead">
            {loaded
              ? "Another formula queues behind the one the lab has."
              : "The lab is waiting to be asked. The formula you pick starts the bench scan."}
          </p>
          <label className="picker__batch">
            Batch
            <input
              type="number"
              min="0.1"
              max="10"
              step="0.1"
              value={batch}
              onChange={(e) => setBatch(Number(e.target.value))}
            />
            g
          </label>
          <ol className="picker__list">
            {formulas.map((f) => (
              <li key={f.id} className="picker-row">
                <span className="chip">{f.id}</span>
                <span className="picker-row__name" title={f.description ?? f.name}>{f.name}</span>
                <span className="picker-row__meta">{f.family} · {f.ingredients} compounds</span>
                <button
                  type="button"
                  className="view-toggle"
                  disabled={!ready || busy !== null}
                  title={ready ? `Send ${f.id} to the robot` : "The lab is still starting up"}
                  onClick={() => send(f)}
                >
                  {busy === f.id ? "Sending…" : loaded ? "Queue" : "Load"}
                </button>
              </li>
            ))}
          </ol>
          {reply ? <p className="picker__reply">{reply}</p> : null}
        </>
      )}
    </Panel>
  );
}
