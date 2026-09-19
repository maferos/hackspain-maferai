import { useCallback, useEffect, useRef, useState } from "react";
import "./App.css";
import LabPanels from "./LabPanels";
import LabTaskPanel from "./LabTaskPanel";
import PipelinePanel from "./PipelinePanel";
import Splitter from "./Splitter";
import { useLabState } from "./labState";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL ?? "http://localhost:8000";
const WS_URL = BACKEND_URL.replace(/^http/, "ws") + "/ws/tasks";
const DETECTIONS_URL = BACKEND_URL.replace(/^http/, "ws") + "/ws/detections";
const BOXES_KEY = "robot-viewer.boxes";
const STATE_URL = import.meta.env.VITE_STATE_URL ?? "ws://localhost:8765/state";

const DEFAULT_CAMERAS = [
  { id: "robot", label: "Robot camera" },
  { id: "scene", label: "General camera" },
];

// The viewport has two sources, switchable from the header:
//   realtime — the backend's live MuJoCo streams of the scene.
//   replay   — Eloi's Isaac Sim RTX renders (simulation/renders/isaac/open),
//              static images that need no backend.
// Start in Real time on the live MuJoCo streams; ?replay=1 opens in Replay
// (the Isaac stills, which need no backend).
const INITIAL_MODE = new URLSearchParams(window.location.search).get("replay") === "1" ? "replay" : "realtime";
const STILL_CAMERAS = [
  { id: "scene", label: "General camera", src: "/renders/general.jpg" },
  { id: "aisle", label: "Aisle camera", src: "/renders/room_aisle.jpg" },
];

// Views that can be opened and closed from the header, and the sizes the drag
// handles set. Both are remembered in this browser.
const VIEWS = [
  { id: "robot", label: "Robot" },
  { id: "balance", label: "Balance" },
  { id: "tasks", label: "Tasks" },
  { id: "pipeline", label: "Pipeline" },
];
const DEFAULT_SIZES = { tasksWidth: 320, panelsHeight: 230, robotShare: 0.5, pipelineHeight: 300 };
const DEFAULT_LAYOUT = {
  ...DEFAULT_SIZES,
  views: Object.fromEntries(VIEWS.map((v) => [v.id, true])),
};
const LAYOUT_KEY = "robot-viewer.layout";
const SPLITTER_PX = 16;

function loadLayout() {
  try {
    const saved = JSON.parse(localStorage.getItem(LAYOUT_KEY));
    if (saved) return { ...DEFAULT_LAYOUT, ...saved, views: { ...DEFAULT_LAYOUT.views, ...saved.views } };
  } catch {
    /* no storage: start from the default layout */
  }
  return DEFAULT_LAYOUT;
}

const clamp = (x, lo, hi) => Math.min(Math.max(x, lo), Math.max(lo, hi));

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

// The detector's boxes over a camera, in the frame's own pixels: the viewBox is
// the frame and "slice" crops it exactly as the image's object-fit: cover does.
function DetectionBoxes({ detections }) {
  return (
    <svg
      className="camera-frame__boxes"
      viewBox={`0 0 ${detections.width} ${detections.height}`}
      preserveAspectRatio="xMidYMid slice"
      aria-hidden="true"
    >
      {detections.boxes.map(([x0, y0, x1, y1], i) => (
        <rect key={i} x={x0 - 3} y={y0 - 3} width={x1 - x0 + 6} height={y1 - y0 + 6} />
      ))}
    </svg>
  );
}

// Live boxes from the backend's detector, while `enabled`; the backend runs the
// model only while someone is connected.
function useDetections(enabled) {
  const [detections, setDetections] = useState(null);
  useEffect(() => {
    if (!enabled) return;
    let cancelled = false;
    let retryTimer;
    let ws;
    const connect = () => {
      ws = new WebSocket(DETECTIONS_URL);
      ws.onmessage = (event) => {
        if (cancelled) return;
        try {
          const payload = JSON.parse(event.data);
          if (Array.isArray(payload.boxes)) setDetections(payload);
        } catch {
          /* ignore malformed frame */
        }
      };
      ws.onclose = () => {
        if (!cancelled) retryTimer = setTimeout(connect, 1500);
      };
      ws.onerror = () => ws.close();
    };
    connect();
    return () => {
      cancelled = true;
      clearTimeout(retryTimer);
      ws?.close();
      setDetections(null);
    };
  }, [enabled]);
  return enabled ? detections : null;
}

function LiveCameraImage({ cameraId, label }) {
  const imageRef = useRef(null);
  const [connected, setConnected] = useState(false);
  useEffect(() => {
    const img = imageRef.current;
    let cancelled = false;
    let socket;
    let retry;
    let currentUrl;
    let pendingUrl;
    const connect = () => {
      socket = new WebSocket(`${BACKEND_URL.replace(/^http/, "ws")}/ws/camera/${cameraId}`);
      socket.binaryType = "blob";
      socket.onmessage = ({ data }) => {
        // Keep only one image decoding at a time; slow clients skip frames.
        if (cancelled || pendingUrl || !(data instanceof Blob)) return;
        if (!img) return;
        pendingUrl = URL.createObjectURL(new Blob([data], { type: "image/jpeg" }));
        img.onload = () => {
          if (currentUrl) URL.revokeObjectURL(currentUrl);
          currentUrl = pendingUrl;
          pendingUrl = null;
          if (!cancelled) setConnected(true);
        };
        img.onerror = () => {
          if (pendingUrl) URL.revokeObjectURL(pendingUrl);
          pendingUrl = null;
          if (!cancelled) setConnected(false);
        };
        img.src = pendingUrl;
      };
      socket.onclose = () => {
        if (cancelled) return;
        setConnected(false);
        retry = setTimeout(connect, 1500);
      };
      socket.onerror = () => socket.close();
    };
    connect();
    return () => {
      cancelled = true;
      clearTimeout(retry);
      socket?.close();
      if (img) {
        img.onload = null;
        img.onerror = null;
      }
      if (pendingUrl) URL.revokeObjectURL(pendingUrl);
      if (currentUrl) URL.revokeObjectURL(currentUrl);
    };
  }, [cameraId]);
  return <>
    <img ref={imageRef} alt={label} className="camera-frame__img" />
    {!connected && <span className="camera-frame__connection" role="status">Connecting camera…</span>}
  </>;
}

function CameraStream({ cameraId, label, className, onClick, big, still, detections }) {
  const boxes = detections && detections.camera === cameraId ? detections : null;
  return (
    <div className={`camera-frame ${className ?? ""}`} onClick={onClick}>
      {still ? <img src={still} alt={label} className="camera-frame__img" />
        : <LiveCameraImage key={cameraId} cameraId={cameraId} label={label} />}
      {boxes && <DetectionBoxes detections={boxes} />}
      <span className="camera-frame__label">
        {label}
        {boxes && ` · ${boxes.boxes.length} bottles`}
      </span>
      {!big && <span className="camera-frame__swap">⇄ swap</span>}
    </div>
  );
}

export default function App() {
  const [mode, setMode] = useState(INITIAL_MODE);
  const realtime = mode === "realtime";
  const [liveCameras, setLiveCameras] = useState(DEFAULT_CAMERAS);
  const cameras = realtime ? liveCameras : STILL_CAMERAS;
  const [mainCameraId, setMainCameraId] = useState(realtime ? "robot" : "scene");
  const [tasks, setTasks] = useState([]);
  const [wsConnected, setWsConnected] = useState(false);
  const wsRef = useRef(null);
  // The lab state feeds the side panels in both modes: the mode only picks the
  // viewport's source. Without a publisher on :8765 the panels play the
  // recorded scripted run (see labState.js).
  const lab = useLabState(STATE_URL);
  const [layout, setLayout] = useState(loadLayout);
  // Boxes are on unless this browser turned them off.
  const [showBoxes, setShowBoxes] = useState(() => {
    try {
      return localStorage.getItem(BOXES_KEY) !== "0";
    } catch {
      return true;
    }
  });
  const [detector, setDetector] = useState(null);
  const detections = useDetections(realtime && showBoxes && detector?.available === true);

  useEffect(() => {
    try {
      localStorage.setItem(BOXES_KEY, showBoxes ? "1" : "0");
    } catch {
      /* the choice just isn't remembered */
    }
  }, [showBoxes]);

  useEffect(() => {
    if (!realtime) return;
    fetch(`${BACKEND_URL}/api/detector`)
      .then((res) => res.json())
      .then(setDetector)
      .catch(() => setDetector(null));
  }, [realtime]);

  useEffect(() => {
    try {
      localStorage.setItem(LAYOUT_KEY, JSON.stringify(layout));
    } catch {
      /* the layout just isn't remembered */
    }
  }, [layout]);

  const resize = (patch) => setLayout((l) => ({ ...l, ...patch }));
  const toggleView = (id) => setLayout((l) => ({ ...l, views: { ...l.views, [id]: !l.views[id] } }));

  // Reset the main viewport to each source's primary camera when the mode flips.
  useEffect(() => {
    setMainCameraId(realtime ? "robot" : "scene");
  }, [realtime]);

  useEffect(() => {
    if (!realtime) return;
    fetch(`${BACKEND_URL}/api/cameras`)
      .then((res) => res.json())
      .then((data) => {
        if (Array.isArray(data) && data.length > 0) setLiveCameras(data);
      })
      .catch(() => {
        /* keep defaults; backend may still be starting up */
      });
  }, [realtime]);

  useEffect(() => {
    if (!realtime) {
      setTasks([]);
      setWsConnected(false);
      return;
    }
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
  }, [realtime]);

  const pipCameraId = cameras.find((c) => c.id !== mainCameraId)?.id ?? mainCameraId;
  const mainLabel = cameras.find((c) => c.id === mainCameraId)?.label ?? mainCameraId;
  const pipLabel = cameras.find((c) => c.id === pipCameraId)?.label ?? pipCameraId;
  const mainStill = cameras.find((c) => c.id === mainCameraId)?.src;
  const pipStill = cameras.find((c) => c.id === pipCameraId)?.src;

  const swapCameras = useCallback(() => setMainCameraId(pipCameraId), [pipCameraId]);

  // With the lab state connected, the task panel shows the formula and the
  // plan; without it, the backend's mocked task log as before.
  const labRunning = lab.state && lab.state.run.status !== "idle" ? lab.state : null;

  const { views } = layout;
  const showPanels = views.robot || views.balance;
  const showSide = views.tasks || views.pipeline;

  // Each handle measures its parent when the drag starts and keeps every view
  // at a usable minimum size.
  const dragTasks = (bar) => {
    const start = layout.tasksWidth;
    const max = start + bar.previousElementSibling.getBoundingClientRect().width - 480;
    return (d) => resize({ tasksWidth: clamp(start - d, 220, max) });
  };
  const dragPanels = (bar) => {
    const start = layout.panelsHeight;
    const max = bar.parentElement.clientHeight - SPLITTER_PX - 150;
    return (d) => resize({ panelsHeight: clamp(start - d, 120, max) });
  };
  const dragPipeline = (bar) => {
    const start = layout.pipelineHeight;
    const max = bar.parentElement.clientHeight - SPLITTER_PX - 200;
    return (d) => resize({ pipelineHeight: clamp(start - d, 140, max) });
  };
  const dragShare = (bar) => {
    const start = layout.robotShare;
    const width = bar.parentElement.clientWidth - SPLITTER_PX;
    return (d) => resize({ robotShare: clamp(start + d / width, 0.2, 0.8) });
  };

  return (
    <div className="app">
      <header className="app__header">
        <div className="app__brand">
          <img src="/mafer-logo.svg" alt="Mafer" className="app__logo" />
          <h1>Robot monitor — mini-Hannover</h1>
        </div>
        <div className="header-controls">
          <div className="mode-toggle" role="group" aria-label="Source">
            <button
              type="button"
              className={`mode-toggle__btn ${realtime ? "mode-toggle__btn--active" : ""}`}
              aria-pressed={realtime}
              onClick={() => setMode("realtime")}
            >
              Real time
            </button>
            <button
              type="button"
              className={`mode-toggle__btn ${!realtime ? "mode-toggle__btn--active" : ""}`}
              aria-pressed={!realtime}
              onClick={() => setMode("replay")}
            >
              Replay
            </button>
          </div>
          <nav className="view-toggles" aria-label="Views">
            {VIEWS.map((v) => (
              <button
                key={v.id}
                type="button"
                className={`view-toggle ${views[v.id] ? "view-toggle--on" : ""}`}
                aria-pressed={views[v.id]}
                title={v.title}
                onClick={() => toggleView(v.id)}
              >
                {v.label}
              </button>
            ))}
            {realtime && (
              <button
                type="button"
                className={`view-toggle ${showBoxes && detector?.available ? "view-toggle--on" : ""}`}
                aria-pressed={showBoxes}
                disabled={!detector?.available}
                title={
                  detector?.available
                    ? `Bottle boxes on the general camera (${detector.weights})`
                    : detector?.error ?? "Bottle detector not reachable"
                }
                onClick={() => setShowBoxes((on) => !on)}
              >
                Boxes
              </button>
            )}
          </nav>
        </div>
      </header>
      <main className="app__body">
        <div className="main-column">
          <section className="viewport">
            <CameraStream
              cameraId={mainCameraId}
              label={mainLabel}
              className="camera-frame--main"
              big
              still={mainStill}
              detections={detections}
            />
            <CameraStream
              cameraId={pipCameraId}
              label={pipLabel}
              className="camera-frame--pip"
              onClick={swapCameras}
              still={pipStill}
              detections={detections}
            />
          </section>
          {showPanels && (
            <Splitter direction="row" onStart={dragPanels} onReset={() => resize({ panelsHeight: DEFAULT_SIZES.panelsHeight })} />
          )}
          {showPanels && (
            <LabPanels
              state={lab.state}
              connected={lab.connected}
              show={views}
              style={{ height: layout.panelsHeight }}
              robotShare={layout.robotShare}
              divider={<Splitter direction="col" onStart={dragShare} onReset={() => resize({ robotShare: DEFAULT_SIZES.robotShare })} />}
            />
          )}
        </div>
        {showSide && (
          <Splitter direction="col" onStart={dragTasks} onReset={() => resize({ tasksWidth: DEFAULT_SIZES.tasksWidth })} />
        )}
        {showSide && (
          <div className="side" style={{ width: layout.tasksWidth }}>
            {views.tasks &&
              (labRunning ? <LabTaskPanel state={labRunning} connected={lab.connected} /> : <TaskPanel tasks={tasks} connected={wsConnected} />)}
            {views.tasks && views.pipeline && (
              <Splitter direction="row" onStart={dragPipeline} onReset={() => resize({ pipelineHeight: DEFAULT_SIZES.pipelineHeight })} />
            )}
            {views.pipeline && (
              <PipelinePanel
                state={lab.state}
                connected={lab.connected}
                style={views.tasks ? { height: layout.pipelineHeight } : { flex: 1 }}
              />
            )}
          </div>
        )}
      </main>
    </div>
  );
}
