import functools
import logging
import pathlib
import string
from functools import lru_cache
from typing import Callable, Coroutine, List, Sequence, Tuple, Type

import anyio

from uidom.web_io import Receive, Scope, Send
from uidom.web_io import WebSocketProtocol as WebSocket

from ._models import WatchPath
from ._notify import Notify
from ._types import ReloadFunc
from ._watch import ChangeSet, FileWatcher

SCRIPT_TEMPLATE_PATH = pathlib.Path(__file__).parent / "script" / "reloader.js"
assert SCRIPT_TEMPLATE_PATH.exists()

logger = logging.getLogger(__name__)


class _Template(string.Template):
    delimiter = "$reloader::"


async def run_until_first_complete(*args: Tuple[Callable, dict]) -> None:
    # this method is taken from starlette
    async with anyio.create_task_group() as task_group:

        async def run(func: Callable[[], Coroutine]) -> None:
            await func()
            task_group.cancel_scope.cancel()

        for func, kwargs in args:
            task_group.start_soon(run, functools.partial(func, **kwargs))


class HotReloadWebSocketRoute:
    def __init__(
        self,
        websocket_type: Type[WebSocket],
        watch_paths: Sequence[WatchPath],
        url_path: str,
        url_name: str,
        reconnect_interval: float = 0.50,
    ) -> None:
        self.websocket_type: Type[WebSocket] = websocket_type
        self.notify = Notify()
        self.watchers = [
            FileWatcher(
                path,
                on_change=functools.partial(self._on_changes, on_reload=on_reload),
            )
            for path, on_reload in watch_paths
        ]
        self._url_path = url_path
        self._url_name = url_name
        self._reconnect_interval = reconnect_interval

    @property
    def url_path(self):
        return self._url_path

    @property
    def url_name(self):
        return self._url_name

    async def _on_changes(
        self, changeset: ChangeSet, *, on_reload: List[ReloadFunc]
    ) -> None:
        description = ", ".join(
            f"file {event} at {', '.join(f'{event!r}' for event in changeset[event])}"
            for event in changeset
        )
        logger.warning("Detected %s. Triggering reload...", description)

        # Run server-side hooks first.
        for callback in on_reload:
            await callback()

        await self.notify.notify()

    @lru_cache
    def script(self) -> str:
        if not hasattr(self, "_script_template"):
            self._script_template = _Template(SCRIPT_TEMPLATE_PATH.read_text())

        content = self._script_template.substitute(
            {"url": self._url_path, "reconnect_interval": self._reconnect_interval}
        )

        return f"<script>{content}</script>"

    async def startup(self) -> None:
        try:
            for watcher in self.watchers:
                await watcher.startup()
        except BaseException as exc:  # pragma: no cover
            logger.error("Error while starting hot reload: %r", exc)
            raise

    async def shutdown(self) -> None:
        try:
            for watcher in self.watchers:
                await watcher.shutdown()
        except BaseException as exc:  # pragma: no cover
            logger.error("Error while stopping hot reload: %r", exc)
            raise

    async def _wait_client_disconnect(self, ws: WebSocket) -> None:
        async for _ in ws.iter_text():
            pass  # pragma: no cover

    async def _watch_reloads(self, ws: WebSocket) -> None:
        async for _ in self.notify.watch():
            await ws.send_text("reload")

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        assert scope["type"] == "websocket"
        ws = self.websocket_type(scope, receive, send)
        await ws.accept()
        await run_until_first_complete(
            (self._watch_reloads, {"ws": ws}),
            (self._wait_client_disconnect, {"ws": ws}),
        )
