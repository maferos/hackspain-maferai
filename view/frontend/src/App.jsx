import { useCallback, useEffect, useRef, useState } from "react";
import replayPatterns from "./replayPatterns.json";
import { chooseScene } from "./sceneSession";
import "./App.css";
import useReplayDetections from "./useReplayDetections";
import FormulaChat from "./FormulaChat";
import LabPanels from "./LabPanels";
import LabTaskPanel from "./LabTaskPanel";
import PipelinePanel from "./PipelinePanel";
import Splitter from "./Splitter";
import { useLabState } from "./labState";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL ?? "http://localhost:8000";
const DETECTIONS_URL = BACKEND_URL.replace(/^http/, "ws") + "/ws/detections";
const BOXES_KEY = "robot-viewer.boxes";
const STATE_URL = import.meta.env.VITE_STATE_URL ?? "ws://localhost:8765/state";

const DEFAULT_CAMERAS = [
  { id: "robot", label: "Robot camera" },
  { id: "scene", label: "General camera" },
];

// The viewport has two sources, switchable from the header:
//   realtime — the backend's live MuJoCo streams of the scene.
//   replay   — synchronized Isaac Lab rail videos for the backend-selected seed.
// Explicit links override the saved mode; new browsers start in Real time.
const MODE_KEY = "robot-viewer.mode";
function loadMode() {
  const replay = new URLSearchParams(window.location.search).get("replay");
  if (replay === "1") return "replay";
  if (replay === "0") return "realtime";
  try {
    return localStorage.getItem(MODE_KEY) === "replay" ? "replay" : "realtime";
  } catch {
    return "realtime";
  }
}
const REPLAY_CAMERAS = [
  { id: "scene", label: "General camera" },
  { id: "robot", label: "Robot camera" },
];

// Views that can be opened and closed from the header, and the sizes the drag
// handles set. Both are remembered in this browser.
const VIEWS = [
  { id: "robot", label: "Robot" },
  { id: "balance", label: "Balance" },
];
const DEFAULT_SIZES = { tasksWidth: 320, panelsHeight: 230, robotShare: 0.5, chatHeight: 240, pipelineHeight: 290 };
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

const clock = (s) => `${String(Math.floor(s / 60)).padStart(2, "0")}:${String(Math.floor(s % 60)).padStart(2, "0")}`;

// One line in the header saying what the lab is doing: the order and its stage,
// else the scan, else that it is idle.
function LabStatus({ state, connected }) {
  if (!connected || !state) {
    return <span className="lab-status lab-status--off">Lab offline</span>;
  }
  const order = state.order;
  if (order && (order.status === "queued" || order.status === "running")) {
    const stage = order.stages.find((s) => s.status === "active");
    return (
      <span className="lab-status lab-status--busy">
        {order.id} · {stage ? stage.label : "Queued"} {order.done}/{order.total} · {clock(order.elapsedSeconds)}
      </span>
    );
  }
  const scan = state.scan;
  if (scan && !scan.done) {
    return (
      <span className="lab-status lab-status--busy">
        Scanning · {scan.named}/{scan.tracked} named
      </span>
    );
  }
  if (order && order.qc) {
    return (
      <span className={`lab-status ${order.qc.passed ? "lab-status--ok" : "lab-status--warn"}`}>
        {order.id} {order.qc.passed ? "complete" : "finished with problems"} · ready
      </span>
    );
  }
  return <span className="lab-status lab-status--ok">{scan ? `Bench mapped · ${scan.named} flasks · ready` : "Ready"}</span>;
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
        <g key={i} className={detections.labels?.[i]?.startsWith("SMP-") ? "scan-identified" : ""}>
          <rect x={x0 - 3} y={y0 - 3} width={x1 - x0 + 6} height={y1 - y0 + 6} />
          {detections.labels?.[i] && <text x={x0 - 3} y={y0 - 10}>{detections.labels[i]}</text>}
        </g>
      ))}
    </svg>
  );
}

function ScanStatus() {
  const [scan, setScan] = useState(null);
  useEffect(() => {
    const controller = new AbortController();
    let timer;
    const update = async () => {
      try {
        const response = await fetch(`${BACKEND_URL}/api/scan`, { signal: controller.signal });
        if (!response.ok) throw new Error("Scan unavailable");
        setScan(await response.json());
      } catch {
        if (!controller.signal.aborted) setScan({ status: "error", error: "Scan connection lost" });
      }
      if (!controller.signal.aborted) timer = setTimeout(update, 1000);
    };
    update();
    return () => { controller.abort(); clearTimeout(timer); };
  }, []);
  if (scan?.status === "disabled") return null;
  return <div className={`scan-status ${scan?.status === "error" ? "scan-status--error" : ""}`} role="status">
    <strong>{scan?.status === "complete" ? "Scan complete" : "Live scan"}</strong>
    <span>{scan?.error || scan?.caption || "Connecting to scan…"}</span>
    {scan?.tracked > 0 && <span>{scan.named} / {scan.tracked} identified</span>}
  </div>;
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
        if (!cancelled) {
          setDetections(null);
          retryTimer = setTimeout(connect, 1500);
        }
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

function LiveCameraImage({ cameraId, label, preview }) {
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
      socket = new WebSocket(`${BACKEND_URL.replace(/^http/, "ws")}/ws/camera/${cameraId}?preview=${preview}`);
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
  }, [cameraId, preview]);
  return <>
    <img ref={imageRef} alt={label} className="camera-frame__img" />
    {!connected && <span className="camera-frame__connection" role="status">Connecting camera…</span>}
  </>;
}

function CameraStream({ cameraId, label, className, onClick, big, detections }) {
  const boxes = detections && detections.camera === cameraId ? detections : null;
  return (
    <div className={`camera-frame ${className ?? ""}`} onClick={onClick}>
      <LiveCameraImage key={`${cameraId}-${big}`} cameraId={cameraId} label={label} preview={!big} />
      {boxes && <DetectionBoxes detections={boxes} />}
      <span className="camera-frame__label">
        {label}
        {boxes && ` · ${boxes.boxes.length} bottles`}
      </span>
      {!big && <span className="camera-frame__swap">⇄ swap</span>}
    </div>
  );
}

function ReplayViewport({ mainCameraId, onSwap, showBoxes, pattern }) {
  const cameras = REPLAY_CAMERAS.map((camera) => ({
    ...camera, src: `/renders/seeds/${camera.id === "scene" ? pattern.global_video : pattern.robot_video}${pattern.revision ? `?v=${pattern.revision}` : ""}`,
  }));
  const videos = useRef({});
  const replay = useReplayDetections(videos, showBoxes, BACKEND_URL, pattern.pattern);
  const [error, setError] = useState(false);

  useEffect(() => {
    const [leader, follower] = REPLAY_CAMERAS.map(({ id }) => videos.current[id]);
    let started = false;
    const start = () => {
      if (started || [leader, follower].some((video) => video.readyState < 3)) return;
      started = true;
      leader.currentTime = follower.currentTime = 0;
      Promise.all([leader.play(), follower.play()]).catch(() => setError(true));
    };
    leader.addEventListener("canplay", start);
    follower.addEventListener("canplay", start);
    start();
    // Keep the same video elements when swapping views, and correct playback
    // drift (including at the loop boundary) against the global camera.
    const timer = window.setInterval(() => {
      if (started && Math.abs(leader.currentTime - follower.currentTime) > 0.1) {
        follower.currentTime = leader.currentTime;
      }
    }, 250);
    return () => {
      clearInterval(timer);
      for (const video of [leader, follower]) {
        video.removeEventListener("canplay", start);
        video.pause();
      }
    };
  }, []);

  return cameras.map(({ id, label, src }) => {
    const big = id === mainCameraId;
    return <div key={id} className={`camera-frame camera-frame--${big ? "main" : "pip"}`}
      onClick={big ? undefined : onSwap}>
      <video ref={(video) => { videos.current[id] = video; }} src={src}
        className="camera-frame__img" aria-label={label} muted loop playsInline
        preload="auto" onError={() => setError(true)} />
      {id === "scene" && replay.boxes && <DetectionBoxes detections={replay.boxes} />}
      <span className="camera-frame__label">{label}</span>
      {error && <span className="camera-frame__connection" role="status">Replay unavailable. Reload to try again.</span>}
      {!big && <span className="camera-frame__swap">⇄ swap</span>}
    </div>;
  });
}

export default function App() {
  const [scenePattern, setScenePattern] = useState(null);
  useEffect(() => {
    let cancelled = false;
    let retry;
    const select = () => chooseScene(BACKEND_URL).then((pattern) => {
      if (!cancelled) setScenePattern(pattern);
    }).catch(() => {
      if (!cancelled) retry = setTimeout(select, 5000);
    });
    select();
    return () => { cancelled = true; clearTimeout(retry); };
  }, []);
  const replayPattern = replayPatterns.find((entry) => entry.seed === scenePattern?.seed);
  const [mode, setMode] = useState(loadMode);
  useEffect(() => {
    try {
      localStorage.setItem(MODE_KEY, mode);
    } catch {
      /* The URL still preserves this tab's selection without storage. */
    }
    const url = new URL(window.location.href);
    url.searchParams.set("replay", mode === "replay" ? "1" : "0");
    window.history.replaceState(window.history.state, "", url);
  }, [mode]);
  const realtime = mode === "realtime";
  const [liveCameras, setLiveCameras] = useState(DEFAULT_CAMERAS);
  const cameras = realtime ? liveCameras : REPLAY_CAMERAS;
  const [mainCameraId, setMainCameraId] = useState("scene");
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
  // Pipeline metrics stay live independently of the viewport's source or boxes.
  const liveDetections = useDetections(
    detector?.available === true,
  );
  const detections = realtime && showBoxes ? liveDetections : null;

  useEffect(() => {
    try {
      localStorage.setItem(BOXES_KEY, showBoxes ? "1" : "0");
    } catch {
      /* the choice just isn't remembered */
    }
  }, [showBoxes]);

  useEffect(() => {
    let cancelled = false;
    let timer;
    const controller = new AbortController();
    const poll = async () => {
      try {
        const res = await fetch(`${BACKEND_URL}/api/detector`, {
          signal: AbortSignal.any([controller.signal, AbortSignal.timeout(4000)]),
        });
        if (!res.ok) throw new Error("Detector unavailable");
        const info = await res.json();
        if (!cancelled) {
          setDetector(info);
          if (info.pattern) setScenePattern(info.pattern);
        }
      } catch {
        if (!cancelled) setDetector(null);
      }
      if (!cancelled) timer = setTimeout(poll, 2000);
    };
    poll();
    return () => {
      cancelled = true;
      controller.abort();
      clearTimeout(timer);
    };
  }, []);

  useEffect(() => {
    try {
      localStorage.setItem(LAYOUT_KEY, JSON.stringify(layout));
    } catch {
      /* the layout just isn't remembered */
    }
  }, [layout]);

  const resize = (patch) => setLayout((l) => ({ ...l, ...patch }));
  const toggleView = (id) => setLayout((l) => ({ ...l, views: { ...l.views, [id]: !l.views[id] } }));

  // Start with the general camera when opening or switching viewport sources.
  useEffect(() => {
    setMainCameraId("scene");
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

  const pipCameraId = cameras.find((c) => c.id !== mainCameraId)?.id ?? mainCameraId;
  const cameraLabel = cameras.find((c) => c.id === mainCameraId)?.label ?? mainCameraId;
  const mainLabel = cameraLabel;
  const pipLabel = cameras.find((c) => c.id === pipCameraId)?.label ?? pipCameraId;

  const swapCameras = useCallback(() => setMainCameraId(pipCameraId), [pipCameraId]);

  // The chat and the header follow the live lab state only, never the recording.
  const live = lab.connected ? lab.state : null;

  const { views } = layout;
  const showPanels = views.robot || views.balance;

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
  const dragChat = (bar) => {
    const start = layout.chatHeight;
    const max = bar.parentElement.clientHeight - layout.pipelineHeight - 2 * SPLITTER_PX - 160;
    return (d) => resize({ chatHeight: clamp(start - d, 160, max) });
  };
  const dragPipeline = (bar) => {
    const start = layout.pipelineHeight;
    const max = bar.parentElement.clientHeight - layout.chatHeight - 2 * SPLITTER_PX - 160;
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
          <LabStatus state={live} connected={lab.connected} />
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
            {(
              <button
                type="button"
                className={`view-toggle ${showBoxes && (!realtime || detector?.available) ? "view-toggle--on" : ""}`}
                aria-pressed={showBoxes}
                disabled={realtime && !detector?.available}
                title={
                  !realtime ? "Predictive YOLO boxes on the replay general camera" : detector?.available
                    ? `Bottle boxes on the general camera (${detector.weights})`
                    : detector?.error ?? "Bottle detector not reachable"
                }
                onClick={() => {
                  if (!showBoxes) setMainCameraId("scene");
                  setShowBoxes((on) => !on);
                }}
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
            {realtime ? <>
              <ScanStatus />
              <CameraStream
                cameraId={mainCameraId}
                label={mainLabel}
                className="camera-frame--main"
                big
                detections={detections}
              />
              <CameraStream
                cameraId={pipCameraId}
                label={pipLabel}
                className="camera-frame--pip"
                onClick={swapCameras}
                detections={detections}
              />
            </> : replayPattern ? <ReplayViewport key={`${replayPattern.pattern}:${replayPattern.revision ?? "original"}`} pattern={replayPattern} mainCameraId={mainCameraId} onSwap={swapCameras} showBoxes={showBoxes} />
              : <div className="camera-frame camera-frame--main"><span className="camera-frame__connection" role="status">
                {scenePattern ? `Replay unavailable for seed ${scenePattern.seed}` : "Waiting for the current seed… Connect the backend to select a layout."}
              </span></div>}
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
        <Splitter direction="col" onStart={dragTasks} onReset={() => resize({ tasksWidth: DEFAULT_SIZES.tasksWidth })} />
        <div className="side" style={{ width: layout.tasksWidth }}>
          <LabTaskPanel state={lab.state} connected={lab.connected} />
          <Splitter direction="row" onStart={dragChat} onReset={() => resize({ chatHeight: DEFAULT_SIZES.chatHeight })} />
          <FormulaChat backendUrl={BACKEND_URL} lab={live} style={{ height: layout.chatHeight }} />
          <Splitter direction="row" onStart={dragPipeline} onReset={() => resize({ pipelineHeight: DEFAULT_SIZES.pipelineHeight })} />
          <PipelinePanel
            state={lab.state}
            connected={lab.connected}
            detections={liveDetections}
            detector={detector}
            style={{ height: layout.pipelineHeight }}
          />
        </div>
      </main>
    </div>
  );
}
