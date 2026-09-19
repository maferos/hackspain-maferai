// Subscribes to the LabState websocket published by the backend
// (ws://localhost:8765/state) and keeps the merged state in React.
// Messages: snapshot (full state), state_update (deep-partial patch, arrays
// replace), event (log line) and mass_sample (balance chart point).
//
// Without a live publisher the viewer plays the scripted run it ships with
// (public/scripted-run.json, written by `python -m labbridge.record_run`), so
// the panels show the formulation on any machine. It loops, holding the
// finished run for a few seconds.
import { useEffect, useState } from "react";

const isObject = (x) => x !== null && typeof x === "object" && !Array.isArray(x);

export function deepMerge(base, patch) {
  if (!isObject(base) || !isObject(patch)) return patch;
  const out = { ...base };
  for (const [key, value] of Object.entries(patch)) {
    out[key] = isObject(value) && isObject(out[key]) ? deepMerge(out[key], value) : value;
  }
  return out;
}

export function applyMessage(state, msg) {
  switch (msg.type) {
    case "snapshot":
      return msg.state;
    case "state_update":
      return state && msg.patch ? deepMerge(state, msg.patch) : state;
    case "event":
      return state ? { ...state, events: [...(state.events ?? []), msg].slice(-50) } : state;
    case "mass_sample":
      return state
        ? { ...state, balance: { ...state.balance, history: [...(state.balance.history ?? []), msg].slice(-600) } }
        : state;
    default:
      return state;
  }
}

const RECORDING_URL = "/scripted-run.json";
const HOLD_S = 10;
const TICK_MS = 100;

// The recorder reduces a list of records to {"$changed": {index: record}};
// rebuild it from the list the state already has.
function expand(patch, base) {
  if (isObject(patch) && isObject(patch.$changed) && Array.isArray(base)) {
    const out = [...base];
    for (const [i, item] of Object.entries(patch.$changed)) out[Number(i)] = item;
    return out;
  }
  if (!isObject(patch)) return patch;
  const out = {};
  for (const [key, value] of Object.entries(patch)) out[key] = expand(value, isObject(base) ? base[key] : undefined);
  return out;
}

function useRecordedRun(enabled) {
  const [state, setState] = useState(null);

  useEffect(() => {
    if (!enabled) return;
    let cancelled = false;
    let timer;

    fetch(RECORDING_URL)
      .then((res) => res.json())
      .then((rec) => {
        if (cancelled) return;
        const start = performance.now();
        let loop = -1;
        let next = 0;
        let current = null;
        const tick = () => {
          const elapsed = (performance.now() - start) / 1000;
          const period = rec.duration + HOLD_S;
          const n = Math.floor(elapsed / period);
          const t = Math.min(elapsed - n * period, rec.duration);
          let s = current;
          if (n !== loop) {
            loop = n;
            next = 0;
            s = rec.snapshot;
          }
          while (next < rec.messages.length && rec.messages[next].time <= t) {
            const msg = rec.messages[next++];
            s = applyMessage(s, msg.type === "state_update" ? { ...msg, patch: expand(msg.patch, s) } : msg);
          }
          if (s !== current) {
            current = s;
            setState(s);
          }
        };
        tick();
        timer = setInterval(tick, TICK_MS);
      })
      .catch(() => {
        /* no recording: the panels say the lab state is offline */
      });

    return () => {
      cancelled = true;
      clearInterval(timer);
    };
  }, [enabled]);

  return enabled ? state : null;
}

export function useLabState(url) {
  const [state, setState] = useState(null);
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    if (!url) {
      setState(null);
      setConnected(false);
      return;
    }
    let cancelled = false;
    let retryTimer;
    let ws;

    const connect = () => {
      ws = new WebSocket(url);
      ws.onopen = () => !cancelled && setConnected(true);
      ws.onmessage = (event) => {
        if (cancelled) return;
        try {
          const msg = JSON.parse(event.data);
          setState((prev) => applyMessage(prev, msg));
        } catch {
          /* ignore malformed frame */
        }
      };
      ws.onclose = () => {
        if (cancelled) return;
        setConnected(false);
        retryTimer = setTimeout(connect, 1500);
      };
      ws.onerror = () => ws.close();
    };

    connect();
    return () => {
      cancelled = true;
      clearTimeout(retryTimer);
      ws?.close();
    };
  }, [url]);

  const recorded = useRecordedRun(!connected);
  return connected ? { state, connected } : { state: recorded, connected: false };
}
