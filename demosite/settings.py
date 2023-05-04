# Copyright (c) 2023 UiDOM
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from functools import partial
from pathlib import Path

from starlette.config import Config
from starlette.websockets import WebSocket

from uidom import WebAssets

# from uidom.scripts import cdn

BASE_DIR = Path(__file__).parent

# load .env file contents
config = Config(BASE_DIR / ".env")

# set debug variable
DEBUG = config("DEBUG", cast=bool, default=False)

# defining webassets
webassets = WebAssets(base_dir=BASE_DIR, sub_dir="assets")

# cdn2static = partial(
#     cdn.CDNToStatic,
#     static_dir=webassets.STATIC_JS_DIR,
#     static_url=webassets.url.STATIC_JS_URL,
# )

# unpkg_static = cdn2static(base_url="https://unpkg.com")
# jsdelivr_static = cdn2static(base_url="https://cdn.jsdelivr.net/npm")

# alpinejs_static = jsdelivr_static / "alpinejs"
# htmx_static = unpkg_static / "htmx.org"

# htmx_js = htmx_static["@1.8.6/dist/htmx.min.js"]
# alpine_js = alpinejs_static["@3.12.0/dist/cdn.min.js"]

if DEBUG:
    from uidom import reloader

    # hot reloading via websocket instance

    async def tailwind_watcher():
        from demosite.tailwindcss import tailwind

        await tailwind.async_run()

    hot_reload_route = reloader.HotReloadWebSocketRoute(
        websocket_type=WebSocket,
        watch_paths=[
            reloader.WatchPath("./demosite", on_reload=[tailwind_watcher]),
            reloader.WatchPath("./uidom"),
        ],
        url_path="/hot-reload",
        url_name="hot_reload",
        reconnect_interval=1,
    )
