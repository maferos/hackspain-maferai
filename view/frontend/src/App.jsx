import { useCallback, useEffect, useRef, useState } from "react";
import "./App.css";
import LabPanels from "./LabPanels";
import LabTaskPanel from "./LabTaskPanel";
import { useLabState } from "./labState";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL ?? "http://localhost:8000";
const WS_URL = BACKEND_URL.replace(/^http/, "ws") + "/ws/tasks";
const STATE_URL = import.meta.env.VITE_STATE_URL ?? "ws://localhost:8765/state";

const DEFAULT_CAMERAS = [
  { id: "robot", label: "Robot camera" },
  { id: "scene", label: "General camera" },
];

// By default the viewport shows Eloi's Isaac Sim RTX renders of the scene's
// cameras (simulation/renders/isaac/full); ?live=1 shows the backend's live
// MuJoCo streams instead.
const LIVE = new URLSearchParams(window.location.search).get("live") === "1";
const STILL_CAMERAS = [
  { id: "scene", label: "General camera · Isaac RTX render", src: "/renders/general.jpg" },
  { id: "aisle", label: "Aisle camera · Isaac RTX render", src: "/renders/room_aisle.jpg" },
];

function statusLabel(status) {
  return status === "active" ? "In progress" : "Done";
}

function formatTime(iso) {
  try {
    return new Date(iso).toLocaleTimeString("en-GB", { hour: "2-digit", minute: "2-digit", second: "2-digit" });
  } catch {
    return "";
  }
}

function TaskPanel({ tasks, connected }) {
  const ordered = [...tasks].reverse();
  return (
    <aside className="task-panel">
      <header className="task-panel__header">
        <h2>Robot tasks</h2>
        <span className={`status-dot ${connected ? "status-dot--live" : "status-dot--off"}`} />
      </header>
      <ol className="task-list">
        {ordered.map((task) => (
          <li key={task.id} className={`task-item task-item--${task.status}`}>
            <span className="task-item__marker" />
            <div className="task-item__body">
              <p className="task-item__label">{task.label}</p>
              <p className="task-item__meta">
                {statusLabel(task.status)} · {formatTime(task.started_at)}
              </p>
            </div>
          </li>
        ))}
        {ordered.length === 0 && <li className="task-item task-item--empty">Waiting for tasks…</li>}
      </ol>
    </aside>
  );
}

function CameraStream({ cameraId, label, className, onClick, big, still }) {
  const src = still ?? `${BACKEND_URL}/stream/${cameraId}`;
  return (
    <div className={`camera-frame ${className ?? ""}`} onClick={onClick}>
      <img key={cameraId} src={src} alt={label} className="camera-frame__img" />
      <span className="camera-frame__label">{label}</span>
      {!big && <span className="camera-frame__swap">⇄ swap</span>}
    </div>
  );
}

export default function App() {
  const [cameras, setCameras] = useState(LIVE ? DEFAULT_CAMERAS : STILL_CAMERAS);
  const [mainCameraId, setMainCameraId] = useState(LIVE ? "robot" : "scene");
  const [tasks, setTasks] = useState([]);
  const [wsConnected, setWsConnected] = useState(false);
  const wsRef = useRef(null);
  const lab = useLabState(STATE_URL);

  useEffect(() => {
    if (!LIVE) return;
    fetch(`${BACKEND_URL}/api/cameras`)
      .then((res) => res.json())
      .then((data) => {
        if (Array.isArray(data) && data.length > 0) setCameras(data);
      })
      .catch(() => {
        /* keep defaults; backend may still be starting up */
      });
  }, []);

  useEffect(() => {
    let cancelled = false;
    let retryTimer;

    const connect = () => {
      const ws = new WebSocket(WS_URL);
      wsRef.current = ws;
      ws.onopen = () => !cancelled && setWsConnected(true);
      ws.onmessage = (event) => {
        if (cancelled) return;
        try {
          const payload = JSON.parse(event.data);
          if (Array.isArray(payload.tasks)) setTasks(payload.tasks);
        } catch {
          /* ignore malformed frame */
        }
      };
      ws.onclose = () => {
        if (cancelled) return;
        setWsConnected(false);
        retryTimer = setTimeout(connect, 1500);
      };
      ws.onerror = () => ws.close();
    };

    connect();
    return () => {
      cancelled = true;
      clearTimeout(retryTimer);
      wsRef.current?.close();
    };
  }, []);

  const pipCameraId = cameras.find((c) => c.id !== mainCameraId)?.id ?? mainCameraId;
  const mainLabel = cameras.find((c) => c.id === mainCameraId)?.label ?? mainCameraId;
  const pipLabel = cameras.find((c) => c.id === pipCameraId)?.label ?? pipCameraId;
  const mainStill = cameras.find((c) => c.id === mainCameraId)?.src;
  const pipStill = cameras.find((c) => c.id === pipCameraId)?.src;

  const swapCameras = useCallback(() => setMainCameraId(pipCameraId), [pipCameraId]);

  // With the lab state connected, the task panel shows the formula and the
  // plan; without it, the backend's mocked task log as before.
  const labRunning = lab.state && lab.state.run.status !== "idle" ? lab.state : null;

  return (
    <div className="app">
      <header className="app__header">
        <h1>Robot monitor — mini-Hannover</h1>
      </header>
      <main className="app__body">
        <div className="main-column">
          <section className="viewport">
            <CameraStream cameraId={mainCameraId} label={mainLabel} className="camera-frame--main" big still={mainStill} />
            <CameraStream
              cameraId={pipCameraId}
              label={pipLabel}
              className="camera-frame--pip"
              onClick={swapCameras}
              still={pipStill}
            />
          </section>
          <LabPanels state={lab.state} connected={lab.connected} />
        </div>
        {labRunning ? <LabTaskPanel state={labRunning} connected={lab.connected} /> : <TaskPanel tasks={tasks} connected={wsConnected} />}
      </main>
    </div>
  );
}
