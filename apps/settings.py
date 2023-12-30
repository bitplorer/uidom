
from uidom import WebAssets
from pathlib import Path

HAS_WEB_SOCK = True

try:
    from fastapi.websockets import WebSocket
except ImportError:
    from uidom.web_io import WebSocketProtocol

    class WebSocket(WebSocketProtocol):  # type: ignore
        # this WebSocket is just a placeholder, install websockets, FastAPI or
        # any other library that supports Websocket to actually import it.
        pass
        
    HAS_WEB_SOCK = False
    
BASE_DIR = Path(__file__).parent
DEBUG = True
webassets = WebAssets(base_dir=BASE_DIR, sub_dir="assets", dry_run=not DEBUG)


if DEBUG:
    from uidom import reloader

    # hot reloading via websocket instance

    async def tailwind_watcher():
        from apps.tailwindcss import tailwind

        await tailwind.async_run()

    hot_reload_route = reloader.HotReloadWebSocketRoute(
        websocket_type=WebSocket,
        watch_paths=[
            reloader.WatchPath("./apps", on_reload=[tailwind_watcher]),
        ],
        url_path="/hot-reload",
        url_name="hot_reload",
        reconnect_interval=1,
    )
