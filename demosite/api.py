# Copyright (c) 2022 uidom
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from demosite import settings
from demosite.pages.card import card_router
from demosite.pages.chart import chart_router
from demosite.pages.check_component import testing_api
from demosite.pages.header import header_router
from uidom.htmx import HtmxMiddleware
from uidom.routing.fastapi import DirectoryRouter, HTMLRoute, StreamingRoute

api = FastAPI(
    debug=settings.DEBUG,
    default_response_class=HTMLResponse,
    title="Demosite",
)


api.router.route_class = StreamingRoute
api.include_router(header_router)
api.include_router(chart_router)
api.include_router(card_router)
api.include_router(testing_api)

api.add_middleware(HtmxMiddleware)

if settings.DEBUG:
    # adding browser reloading
    api.add_websocket_route(
        path=settings.hot_reload_route.url_path,
        route=settings.hot_reload_route,
        name=settings.hot_reload_route.url_name,
    )
    api.add_event_handler("startup", settings.hot_reload_route.startup)
    api.add_event_handler("shutdown", settings.hot_reload_route.shutdown)

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
