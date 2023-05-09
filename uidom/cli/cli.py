# Copyright (c) 2023 UiDOM
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


# import black
from pathlib import Path
from string import Template

from typer import Typer

from uidom import WebAssets
from uidom.utils.logger import uidom_logger

project = Typer()


class _Template(Template):
    delimiter = "$variable::"


INDEX_TEMP = _Template(
    """
from uidom.dom import *
from $variable::project_name.document import document

class Index(HTMLElement):
    def render(self, *args, **kwargs):
        return document(div(*args, **kwargs))
"""
)

API_TEMP = _Template(
    """
from $variable::project_name.index import Index

async def home(scope, receive, send):
    assert scope["type"] == "http"
    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [
                [b"content-type", b"text/html"],
            ],
        }
    )
    await send({"type": "http.response.body", "body": str(Index("Hello, world!")).encode()})
    """
)


SERVER_TEMP = _Template(
    """

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "$variable::project_name.api:home",
        host="127.0.0.1",
        port=8081,
        reload=True,
        # ssl_keyfile='../$variable::project_name/key.pem',
        # ssl_certfile='../$variable::project_name/cert.pem'
    )
    """
)


DOCUMENT_TEMP = _Template(
    """
from $variable::project_name import settings
from $variable::project_name.tailwindcss import tailwind
from uidom import UiDOM
from uidom.dom import link, raw

__all__ = ["document"]


document = UiDOM(
    webassets=settings.webassets,
    head=[
        link(href=f"/css/{tailwind.output_css}", rel="stylesheet"),
    ],
    body=[
        raw(settings.hot_reload_route.script() if settings.DEBUG and settings.HAS_WEB_SOCK else ""),
    ],
)
"""
)

SETTINGS_TEMP = _Template(
    """
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
webassets = WebAssets(base_dir=BASE_DIR, sub_dir="$variable::asset_dir")


if DEBUG:
    from uidom import reloader

    # hot reloading via websocket instance

    async def tailwind_watcher():
        from $variable::project_name.tailwindcss import tailwind

        await tailwind.async_run()

    hot_reload_route = reloader.HotReloadWebSocketRoute(
        websocket_type=WebSocket,
        watch_paths=[
            reloader.WatchPath("./$variable::project_name", on_reload=[tailwind_watcher]),
        ],
        url_path="/hot-reload",
        url_name="hot_reload",
        reconnect_interval=1,
    )
"""
)

TAILWIND_TEMP = _Template(
    """
from $variable::project_name import settings
from uidom import TailwindCommand

if settings.DEBUG:
    tailwind = TailwindCommand(
        file_path=__file__,
        webassets=settings.webassets,
        # input_css=settings.INPUT_CSS_FILE,
        # output_css=settings.OUTPUT_CSS_FILE,
        minify=not settings.DEBUG,
    )

if __name__ == "__main__":
    if settings.DEBUG:
        tailwind.run()
"""
)


@project.command()
def create_project(project_name: str, asset_folder: str):
    ":: command for creating new projects"
    if project_name is not None:
        create_permission = str(
            input(f"proceed to create project: {project_name} ? [y/n] ")
        )
        permission = create_permission.lower() == "y"
        if permission:
            project_logger = uidom_logger
            project_logger.info(f" ==creating project== ")
            project_dir = Path(project_name).resolve()
            base_dir = project_dir / asset_folder
            webassets = WebAssets(
                base_dir=base_dir,
                dry_run=not permission,
            )

            # creating settings.py file
            SETTINGS_TEXT = SETTINGS_TEMP.substitute(
                {"project_name": project_name, "asset_dir": asset_folder}
            )
            # SETTINGS_TEXT = black.format_str(SETTINGS_TEXT, mode=black.FileMode())

            settings_file: Path = project_dir / "settings.py"

            if not settings_file.exists():
                with settings_file.open(mode="w") as f:
                    f.write(SETTINGS_TEXT)

                project_logger.info(str(settings_file.name))

            # creating tailwindcss.py file
            TAILWIND_TEXT = TAILWIND_TEMP.substitute({"project_name": project_name})
            # TAILWIND_TEXT = black.format_str(TAILWIND_TEXT, mode=black.FileMode())
            tailwindcss_file: Path = project_dir / "tailwindcss.py"

            if not tailwindcss_file.exists():
                with tailwindcss_file.open(mode="w") as f:
                    f.write(TAILWIND_TEXT)

                project_logger.info(str(tailwindcss_file.name))

            # creating document.py file
            DOCUMENT_TEXT = DOCUMENT_TEMP.substitute({"project_name": project_name})

            document_file: Path = project_dir / "document.py"

            if not document_file.exists():
                with document_file.open(mode="w") as f:
                    f.write(DOCUMENT_TEXT)

                project_logger.info(str(document_file.name))

            # creating server.py
            SERVER_TEXT = SERVER_TEMP.substitute({"project_name": project_name})

            server_file: Path = project_dir / "server.py"

            if not server_file.exists():
                with server_file.open(mode="w") as f:
                    f.write(SERVER_TEXT)

                project_logger.info(str(server_file.name))

            # creating api.py
            API_TEXT = API_TEMP.substitute({"project_name": project_name})

            api_file: Path = project_dir / "api.py"

            if not api_file.exists():
                with api_file.open(mode="w") as f:
                    f.write(API_TEXT)

                project_logger.info(str(api_file.name))

            # creating index.py
            INDEX_TEXT = INDEX_TEMP.substitute({"project_name": project_name})

            index_file: Path = project_dir / "index.py"

            if not index_file.exists():
                with index_file.open(mode="w") as f:
                    f.write(INDEX_TEXT)

                project_logger.info(str(index_file.name))

            project_logger.info(f" ==project created==")
        else:
            project_logger.info("exiting")


uidom = project()

if __name__ == "__main__":
    project()
    # cli(uicli, *sys.argv[1:])
