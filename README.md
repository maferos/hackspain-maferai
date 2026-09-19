# hackspain-maferai

Hackathon project. Two components:

- [`simulation/`](simulation/) — robotic lab-automation simulation with MuJoCo + AutoBio. See [`simulation/README.md`](simulation/README.md).
- [`computer-vision/`](computer-vision/) — computer-vision pipeline: barcode identity, single-camera placement and the vessel detector. See [`computer-vision/README.md`](computer-vision/README.md); the detector choice and its benchmark are in [`computer-vision/docs/BENCHMARK.md`](computer-vision/docs/BENCHMARK.md).
- [`view/`](view/) — robot viewer for the live demo: Isaac Sim renders or live MuJoCo streams, plus task, robot and balance panels. See [`view/README.md`](view/README.md).
- [`dashboard/bridge/`](dashboard/bridge/) — `labbridge`, which publishes the lab state the viewer reads over WebSocket. See [`dashboard/bridge/README.md`](dashboard/bridge/README.md).

See [`AGENTS.md`](AGENTS.md) for the team and conventions.
