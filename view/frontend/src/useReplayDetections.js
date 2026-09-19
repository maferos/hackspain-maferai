import { useEffect, useState } from "react";

// Requests are strictly sequential. Playback owns the clock; inference never
// seeks or pauses the displayed video. The backend decodes its own copy.
export default function useReplayDetections(videos, enabled, backendUrl) {
  const [state, setState] = useState({ boxes: null, status: "" });
  useEffect(() => {
    if (!enabled) return;
    const video = videos.current.scene;
    const socket = new WebSocket(backendUrl.replace(/^http/, "ws") + "/ws/replay-detections");
    let ready = false;
    let busy = false;
    let sentAt = 0;
    let latency = 0.1;
    let pending = [];
    let shown = null;
    let epoch = 0;
    let previous = video.currentTime;
    let generation = 0;
    let requestGeneration = 0;
    let animation;
    let status = "Loading replay YOLO…";
    const clock = () => {
      const now = video.currentTime;
      if (previous - now > video.duration / 2) epoch += video.duration;
      previous = now;
      return epoch + now;
    };
    const reset = () => { generation++; pending = []; shown = null; };
    video.addEventListener("seeking", reset);
    socket.onmessage = (event) => {
      const result = JSON.parse(event.data);
      if (result.error) {
        status = result.error;
        ready = false;
        pending = []; shown = null;
      } else if (result.ready) {
        if (Math.abs(result.duration - video.duration) > 0.1) {
          status = "Replay video differs from backend";
          socket.close();
          return;
        }
        ready = true;
      } else {
        latency = Math.min(1, (performance.now() - sentAt) / 1000);
        busy = false;
        if (requestGeneration === generation) {
          pending.push(result);
          pending.sort((a, b) => a.time - b.time);
        }
        status = `YOLO ${result.inference_ms} ms · round trip ${Math.round(latency * 1000)} ms`;
      }
    };
    socket.onclose = () => { ready = false; pending = []; shown = null; status = "Replay detector disconnected"; };
    socket.onerror = () => { status = "Replay detector unavailable"; };
    const tick = () => {
      const now = clock();
      while (pending.length && pending[0].time <= now) {
        const result = pending.shift();
        if (!shown || result.time >= shown.time) shown = result;
      }
      // Never retain old boxes across long inference stalls or a paused seek.
      if (shown && (now - shown.time > 0.5 || shown.time > now)) shown = null;
      if (ready && !busy && !video.paused && !video.seeking && video.readyState >= 2) {
        busy = true;
        sentAt = performance.now();
        requestGeneration = generation;
        socket.send(JSON.stringify({ time: now + latency * video.playbackRate }));
      }
      setState((old) => old.boxes === shown && old.status === status ? old : { boxes: shown, status });
      animation = requestAnimationFrame(tick);
    };
    animation = requestAnimationFrame(tick);
    return () => {
      cancelAnimationFrame(animation);
      video.removeEventListener("seeking", reset);
      socket.onmessage = socket.onclose = socket.onerror = null;
      socket.close();
    };
  }, [videos, enabled, backendUrl]);
  return enabled ? state : { boxes: null, status: "" };
}
