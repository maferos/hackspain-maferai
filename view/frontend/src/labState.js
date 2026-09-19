// Subscribes to the LabState websocket published by the backend
// (ws://localhost:8765/state) and keeps the merged state in React.
// Messages: snapshot (full state), state_update (deep-partial patch, arrays
// replace), event (log line) and mass_sample (balance chart point).
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

export function useLabState(url) {
  const [state, setState] = useState(null);
  const [connected, setConnected] = useState(false);

  useEffect(() => {
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

  return { state, connected };
}
