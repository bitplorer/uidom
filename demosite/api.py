# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from uidom.routing import HTMLRoute, StreamingRoute

from . import settings
from .pages.card import card_router
from .pages.chart import chart_router
from .pages.header import header_router

api = FastAPI(debug=settings.DEBUG, default_response_class=HTMLResponse, title="Demosite")
api.router.route_class = StreamingRoute 
api.include_router(header_router)
api.include_router(chart_router)
api.include_router(card_router)

if settings.DEBUG:
    # adding browser reloading 
    api.add_websocket_route(settings.HOT_RELOAD_URL, route=settings.hot_reload, name=settings.HOT_RELOAD_URL_NAME)
    api.add_event_handler("startup", settings.hot_reload.startup)
    api.add_event_handler("shutdown", settings.hot_reload.shutdown)

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
    StaticFiles(directory=settings.webassets.static.images, check_dir=False),
    name="image",
)
