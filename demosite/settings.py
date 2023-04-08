# Copyright (c) 2023 UiDOM
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from pathlib import Path

from starlette.config import Config

from uidom import FileSettings, WebAssets

BASE_DIR = Path(__file__).parent

# load .env file contents
config = Config(BASE_DIR / ".env")

# set debug variable
DEBUG = config("DEBUG", cast=bool, default=False)

# defining webassets
webassets = WebAssets(FileSettings(BASE_DIR=BASE_DIR, SUB_DIR="assets"))

webassets.
if DEBUG:
    from uidom import reloader

    # hot reloading via websocket instance

    async def tailwind_watcher():
        from demosite.tailwindcss import tailwind

        await tailwind.async_run()

    hot_reload_route = reloader.HotReloadWebSocketRoute(
        watch_paths=[
            reloader.WatchPath("./demosite", on_reload=[tailwind_watcher]),
            reloader.WatchPath("./uidom"),
        ],
        url_path="/hot-reload",
        url_name="hot_reload",
        reconnect_interval=1,
    )
