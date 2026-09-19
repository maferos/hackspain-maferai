"""WebSocket servers that the simulation loop can feed from its own thread.

Each server owns an asyncio loop in a daemon thread. Producers call the
thread-safe ``publish`` helpers; the loop broadcasts to every connected
console. The console reconnects on its own, so servers can be restarted at
will.
"""

from __future__ import annotations

import asyncio
import json
import logging
import threading
from collections import deque
from typing import Any

from websockets.asyncio.server import ServerConnection, broadcast, serve

from labbridge import state as S

logger = logging.getLogger(__name__)


class _WsServer:
    """Threaded WebSocket broadcaster. Subclasses decide what a new client receives."""

    def __init__(self, host: str = "0.0.0.0", port: int = 8765) -> None:
        self.host = host
        self.port = port
        self._loop: asyncio.AbstractEventLoop | None = None
        self._thread: threading.Thread | None = None
        self._ready = threading.Event()
        self._stop: asyncio.Event | None = None
        self._clients: dict[str, set[ServerConnection]] = {}

    # -- lifecycle -----------------------------------------------------------

    def start(self) -> None:
        """Start serving in a background thread; returns once the socket listens."""
        if self._thread is not None:
            return
        self._thread = threading.Thread(target=self._run, name=f"{type(self).__name__}:{self.port}", daemon=True)
        self._thread.start()
        self._ready.wait(timeout=5)

    def stop(self) -> None:
        """Close every connection and stop the loop."""
        if self._loop is None or self._stop is None:
            return
        self._loop.call_soon_threadsafe(self._stop.set)
        if self._thread is not None:
            self._thread.join(timeout=5)
        self._thread = None
        self._loop = None

    def _run(self) -> None:
        asyncio.run(self._serve())

    async def _serve(self) -> None:
        self._loop = asyncio.get_running_loop()
        self._stop = asyncio.Event()
        async with serve(self._handler, self.host, self.port, max_size=None):
            logger.info("%s listening on ws://%s:%d", type(self).__name__, self.host, self.port)
            self._ready.set()
            await self._stop.wait()

    # -- connections ---------------------------------------------------------

    def _group_of(self, connection: ServerConnection) -> str:
        """Which broadcast group a connection joins; the request path by default."""
        return connection.request.path if connection.request else "/"

    async def _on_connect(self, connection: ServerConnection, group: str) -> None:
        """Hook: send whatever a fresh client needs."""

    async def _handler(self, connection: ServerConnection) -> None:
        group = self._group_of(connection)
        self._clients.setdefault(group, set()).add(connection)
        logger.info("client joined %s (%d)", group, len(self._clients[group]))
        try:
            await self._on_connect(connection, group)
            async for _ in connection:  # incoming messages are ignored
                pass
        except Exception:  # noqa: BLE001 - a client dropping is not an error
            pass
        finally:
            self._clients[group].discard(connection)
            logger.info("client left %s (%d)", group, len(self._clients[group]))

    def _broadcast(self, group: str | None, message: str | bytes) -> None:
        """Send to one group (or all groups when ``group`` is None), from any thread."""
        if self._loop is None:
            return

        def _send() -> None:
            targets = self._clients.get(group, set()) if group is not None else {c for cs in self._clients.values() for c in cs}
            if targets:
                broadcast(targets, message)

        self._loop.call_soon_threadsafe(_send)

    @property
    def clients(self) -> int:
        return sum(len(cs) for cs in self._clients.values())


class StateServer(_WsServer):
    """Broadcasts ``LabState`` messages; keeps the last snapshot for new clients.

    Example::

        server = StateServer(port=8765)
        server.start()
        server.snapshot(initial_state)             # once, when the run starts
        server.patch({"robot": {"fsmState": "DOSING"}, "balance": {"netMass": 1.842}})
        server.mass_sample(t, 1.842)
        server.event(t, "controller switched FAST -> SLOW")

    The console connects to ``ws://host:port/state`` (any path is accepted).
    """

    def __init__(self, host: str = "0.0.0.0", port: int = 8765, keep_events: int = 12, keep_samples: int = 600) -> None:
        super().__init__(host, port)
        self.keep_samples = keep_samples
        self._state: dict | None = None
        self._recent_events: deque[dict] = deque(maxlen=keep_events)

    def _group_of(self, connection: ServerConnection) -> str:
        return "state"

    async def _on_connect(self, connection: ServerConnection, group: str) -> None:
        if self._state is not None:
            await connection.send(json.dumps(S.snapshot(self._state)))
            for ev in self._recent_events:
                await connection.send(json.dumps(ev))

    def snapshot(self, state: dict, timestamp: float | None = None) -> None:
        """Replace the whole state on every client."""
        self._state = state
        self._recent_events.clear()
        self._broadcast("state", json.dumps(S.snapshot(state, timestamp)))

    def patch(self, patch: dict, timestamp: float | None = None) -> None:
        """Deep-merge ``patch`` into the state on every client (arrays replace)."""
        if self._state is not None:
            self._state = S.deep_merge(self._state, patch)
        self._broadcast("state", json.dumps(S.state_update(patch, timestamp)))

    def event(self, time: float, message: str, level: str = "info") -> None:
        """Append one line to the event log."""
        ev = S.event(time, message, level)
        self._recent_events.append(ev)
        self._broadcast("state", json.dumps(ev))

    def mass_sample(self, time: float, mass: float) -> None:
        """Append one balance reading to the chart history.

        The sample is also kept in the server's copy of the state, so a console
        that connects later gets the chart in its snapshot.
        """
        sample = {"time": float(time), "mass": float(mass)}
        if self._state is not None:
            balance = self._state.setdefault("balance", {})
            history = list(balance.get("history") or [])
            history.append(sample)
            balance["history"] = history[-self.keep_samples :]
        self._broadcast("state", json.dumps({"type": "mass_sample", **sample}))

    @property
    def state(self) -> dict | None:
        """The state as the console should currently see it."""
        return self._state


class FrameServer(_WsServer):
    """Broadcasts camera frames; clients subscribe by path ``/frames/<camera>``.

    Example::

        frames = FrameServer(port=8766)
        frames.start()
        frames.push("general", jpeg_bytes)   # console: ?sim=ws://host:8766/frames/general

    Frames are sent as binary messages; the console decodes JPEG or PNG.
    """

    def __init__(self, host: str = "0.0.0.0", port: int = 8766) -> None:
        super().__init__(host, port)
        self._last: dict[str, bytes] = {}

    def _group_of(self, connection: ServerConnection) -> str:
        path = connection.request.path if connection.request else "/"
        return path.rstrip("/").split("/")[-1] or "default"

    async def _on_connect(self, connection: ServerConnection, group: str) -> None:
        # A console that joins between frames sees the last one right away.
        last = self._last.get(group)
        if last is not None:
            await connection.send(last)

    def push(self, camera: str, image: bytes) -> None:
        """Send one encoded frame to the clients watching ``camera``."""
        self._last[camera] = image
        self._broadcast(camera, image)

    def push_json(self, camera: str, payload: dict[str, Any]) -> None:
        """Send a ``{"type": "frame", "data": <base64>, "mime": ...}`` frame instead."""
        self._broadcast(camera, json.dumps(payload))
