"""Entry point: `python -m armlab` from `simulation/`.

    python -m armlab                                  console on :8080
    python -m armlab --policy act_transfer_cube       load a checkpoint at startup
    python -m armlab --headless --prompt "..."        run one instruction and exit
"""

from __future__ import annotations

import argparse
import sys
import time

from armlab.runtime import Runtime, spawn
from armlab.scene import DEFAULT_SCENE


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog='armlab', description=__doc__.splitlines()[0])
    parser.add_argument('--scene', default=str(DEFAULT_SCENE))
    parser.add_argument('--policy', help='catalogue key or Hugging Face repo id to preload')
    parser.add_argument('--port', type=int, default=8080)
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--headless', action='store_true',
                        help='run one --prompt to completion and exit, no server')
    parser.add_argument('--prompt', help='instruction to run under --headless')
    parser.add_argument('--seconds', type=float, default=20.0,
                        help='how long a bare --policy run lasts under --headless')
    parser.add_argument('--timeout', type=float, default=300.0)
    parser.add_argument('--fast', action='store_true',
                        help='step as fast as the machine allows instead of real time')
    return parser.parse_args()


def run_headless(args: argparse.Namespace) -> int:
    runtime, _ = spawn(scene_path=args.scene, policy_name=args.policy,
                       realtime=not args.fast)
    if args.prompt:
        runtime.prompt(args.prompt)
    elif args.policy:
        _await_policy(runtime, args.timeout)
        runtime.run_policy(args.seconds)
    else:
        print('--headless needs --prompt or --policy', file=sys.stderr)
        return 2

    deadline = time.time() + args.timeout
    while time.time() < deadline:
        time.sleep(1.0)
        telemetry = runtime.telemetry()
        plan = telemetry['plan']
        if plan and all(step['status'] in ('done', 'failed') for step in plan):
            break
    else:
        print('timed out', file=sys.stderr)

    telemetry = runtime.telemetry()
    runtime.stop()
    for step in telemetry['plan']:
        print(f"  {step['status']:7s} {step['label']}"
              + (f"  -- {step['detail']}" if step['detail'] else ''))
    if policy := telemetry['policy']:
        if policy.get('state') == 'loaded':
            print(f"  policy {policy['repo_id']} ({policy['type']}, "
                  f"{policy['action_dim']}-dim) at {policy['latency_ms']} ms/chunk")
    print(f"  sim ran at x{telemetry['speed']:.2f} real time")
    failed = [s for s in telemetry['plan'] if s['status'] == 'failed']
    return 1 if failed or not telemetry['plan'] else 0


def _await_policy(runtime: Runtime, timeout: float) -> None:
    """Block until the checkpoint has downloaded, migrated and validated."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        state = runtime.telemetry()['policy'].get('state')
        if state in ('loaded', 'error'):
            return
        time.sleep(1.0)


def main() -> int:
    args = parse_args()
    if args.headless:
        return run_headless(args)

    import uvicorn

    from armlab.server import build

    runtime, _ = spawn(scene_path=args.scene, policy_name=args.policy,
                       realtime=not args.fast)
    print(f'armlab console on http://{args.host}:{args.port}')
    # timeout_graceful_shutdown is load-bearing, not a nicety. On SIGTERM uvicorn
    # closes the listener and then waits for open responses to finish -- and an
    # MJPEG stream never finishes on its own. Without a cap the console ignores
    # SIGTERM for as long as a browser tab is watching, and only `kill -9` ends
    # it. Installing our own signal handler would not help: uvicorn replaces the
    # handlers when it starts.
    uvicorn.run(build(runtime), host=args.host, port=args.port, log_level='warning',
                timeout_graceful_shutdown=5)
    runtime.stop()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
