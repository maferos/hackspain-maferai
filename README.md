# hackspain-maferai

Hackathon project. Two components:

- [`simulation/`](simulation/) — robotic lab-automation simulation with MuJoCo + AutoBio. See [`simulation/README.md`](simulation/README.md).
- [`computer-vision/`](computer-vision/) — computer-vision pipeline: barcode identity, single-camera placement and the vessel detector. See [`computer-vision/README.md`](computer-vision/README.md); the detector choice and its benchmark are in [`computer-vision/docs/BENCHMARK.md`](computer-vision/docs/BENCHMARK.md).
- [`dashboard/`](dashboard/) — mission-control console for the live demo (React + Vite). Runs on a deterministic demo replay and connects to the real system over WebSocket or SSE. See [`dashboard/README.md`](dashboard/README.md).

See [`AGENTS.md`](AGENTS.md) for the team and conventions.
