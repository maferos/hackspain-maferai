// A small panel in the dock saying what the viewer is running: which YOLO
// weights the scan and the boxes use and at what threshold, how long the last
// inference took, which chat and executor are behind the formula panel, which
// bench layout is loaded, and the commit. The header's Info button opens and
// closes it.
import { useEffect, useState } from "react";
import { Panel } from "./LabPanels";

function Line({ label, value, title }) {
  return (
    <div className="info-line" title={title}>
      <span className="info-line__label">{label}</span>
      <span className="info-line__value">{value}</span>
    </div>
  );
}

export default function InfoPanel({ backendUrl, detections }) {
  const [info, setInfo] = useState(null);

  useEffect(() => {
    let cancelled = false;
    let timer;
    const poll = () =>
      fetch(`${backendUrl}/api/info`)
        .then((res) => res.json())
        .then((data) => !cancelled && setInfo(data))
        .catch(() => !cancelled && setInfo(null))
        .finally(() => {
          if (!cancelled) timer = setTimeout(poll, 10000);
        });
    poll();
    return () => {
      cancelled = true;
      clearTimeout(timer);
    };
  }, [backendUrl]);

  if (!info) {
    return (
      <Panel title="Info" className="panel--info">
        <p className="pipeline__empty">Backend not reachable</p>
      </Panel>
    );
  }
  const { detector, chat, scene } = info;
  // While the scan runs it owns perception, so its weights are what the boxes are.
  const weights = info.scan.weights ?? detector.weights;
  const conf = info.scan.weights ? info.scan.conf : detector.conf;
  const shared = !info.scan.weights || info.scan.weights === detector.weights;
  return (
    <Panel
      title="Info"
      right={info.build ? <span className="chip" title="the commit this backend runs">{info.build}</span> : null}
      className="panel--info"
    >
      <Line
        label="Detector"
        value={weights ?? "none"}
        title={detector.error ?? `backend ${detector.backend}, on the ${detector.camera} camera at ${detector.input}`}
      />
      <Line
        label="Threshold"
        value={conf != null ? conf.toFixed(2) : "—"}
        title="the score a box needs to be drawn"
      />
      {shared ? null : <Line label="Boxes" value={detector.weights ?? "none"} title="the scan and the boxes are on different models" />}
      <Line
        label="Inference"
        value={detections?.inference_ms ? `${detections.inference_ms} ms · ${detections.boxes.length} boxes` : "—"}
        title="the last measured inference on the general camera"
      />
      <Line
        label="Chat"
        value={chat.model ?? (chat.mode === "offline" ? "offline parser" : chat.mode)}
        title={chat.model ? "Claude reads free-form requests" : "no ANTHROPIC_API_KEY on the backend"}
      />
      <Line label="Executor" value={info.executor ?? "—"} title="who carries the formula out" />
      <Line
        label="Bench"
        value={scene.pattern ? `${scene.pattern} · seed ${scene.seed} · ${scene.count} flasks` : scene.file}
        title={scene.file}
      />
    </Panel>
  );
}
