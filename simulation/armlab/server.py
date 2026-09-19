"""The console: static UI, MJPEG camera streams, and a command WebSocket.

Port 8080 -- 8765/8766 belong to `dashboard/bridge/labbridge` and 8000 was the
since-removed `view/` prototype, so nothing here collides with either.

The handlers never touch MuJoCo. They hand out whatever bytes the sim thread last
published, because a Renderer's GL context belongs to the thread that created it
and rendering from the request pool yields black frames -- the lesson the removed
prototype left behind in `git show 0063523^:view/backend/server.py`.
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, StreamingResponse

from armlab import policies
from armlab.runtime import STREAM_FPS, Runtime

WEB = Path(__file__).resolve().parent / 'web'
#: Short names for the URL; the values are MuJoCo camera names, which contain
#: the arm-attach prefixes and so are awkward in a path.
CAMERAS = {'top': 'top', 'wrist': 'l/wrist_cam_left', 'overview': 'general'}
TELEMETRY_HZ = 5.0


def build(runtime: Runtime) -> FastAPI:
    app = FastAPI(title='armlab console')

    @app.get('/', response_class=HTMLResponse)
    async def index() -> str:
        return (WEB / 'index.html').read_text()

    @app.get('/catalogue')
    async def catalogue() -> dict:
        return {'policies': [{'key': key, **{f: getattr(spec, f) for f in
                                             ('repo_id', 'label', 'embodiment', 'control_hz')}}
                             for key, spec in policies.catalogue().items()]}

    @app.get('/stream/{camera}')
    async def stream(camera: str) -> StreamingResponse:
        name = CAMERAS.get(camera, camera)

        async def frames():
            # Bounded by the runtime, not `while True`: an MJPEG response never
            # ends on its own, and uvicorn's graceful shutdown waits for open
            # responses to finish. An unbounded generator here makes the console
            # ignore SIGTERM for as long as a browser tab is watching.
            while runtime.running:
                jpeg = runtime.frame(name)
                if jpeg:
                    yield (b'--frame\r\nContent-Type: image/jpeg\r\n'
                           b'Content-Length: ' + str(len(jpeg)).encode() + b'\r\n\r\n'
                           + jpeg + b'\r\n')
                await asyncio.sleep(1.0 / STREAM_FPS)

        return StreamingResponse(frames(),
                                 media_type='multipart/x-mixed-replace; boundary=frame')

    @app.websocket('/ws')
    async def socket(ws: WebSocket) -> None:
        await ws.accept()

        async def push() -> None:
            while runtime.running:
                await ws.send_text(json.dumps({'type': 'telemetry', **runtime.telemetry()}))
                await asyncio.sleep(1.0 / TELEMETRY_HZ)

        async def pull() -> None:
            while runtime.running:
                command = json.loads(await ws.receive_text())
                if command.get('type') == 'prompt':
                    runtime.prompt(str(command.get('text', '')))
                else:
                    runtime.submit(command)

        pusher = asyncio.create_task(push())
        try:
            await pull()
        except (WebSocketDisconnect, RuntimeError, json.JSONDecodeError):
            pass
        finally:
            pusher.cancel()

    return app
