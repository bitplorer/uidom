from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from apps import settings
from uidom.routing.fastapi import DirectoryRouter, HTMLRoute, StreamingRoute


@asynccontextmanager
async def lifespan(api: FastAPI):
    if settings.DEBUG:
        # adding browser reloading
        api.add_websocket_route(
            path=settings.hot_reload_route.url_path,
            route=settings.hot_reload_route,
            name=settings.hot_reload_route.url_name,
        )
    if settings.DEBUG:
        await settings.hot_reload_route.startup()
    yield
    if settings.DEBUG:
        await settings.hot_reload_route.shutdown()


api = FastAPI(
    debug=settings.DEBUG,
    default_response_class=HTMLResponse,
    title="apps",
    lifespan=lifespan,
)
api.router.route_class = StreamingRoute
app_router = DirectoryRouter()
api.include_router(app_router)


api.mount(
    "/css",
    StaticFiles(directory=settings.webassets.static.css, check_dir=False),
    name="css",
)
api.mount(
    "/js",
    StaticFiles(directory=settings.webassets.static.js, check_dir=False),
    name="js",
)
api.mount(
    "/image",
    StaticFiles(directory=settings.webassets.static.image, check_dir=False),
    name="image",
)
api.mount(
    "/font",
    StaticFiles(directory=settings.webassets.static.font, check_dir=False),
    name="font",
)
