# Copyright (c) 2023 UiDOM
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from pathlib import Path

from starlette.config import Config

from uidom import FileSettings, WebAssets, arel

# load .env file contents
config = Config(".env")
BASE_DIR = Path(__file__).parent

# hot reloading websocket instance
async def reload_data():
    print("Reloading server data in browser...")
    
hot_reload = arel.HotReload(paths=[arel.Path("./demosite", on_reload=[reload_data]), arel.Path("./uidom", on_reload=[reload_data])])
HOT_RELOAD_URL = "/hot-reload"
HOT_RELOAD_URL_NAME = "hot_reload"
# defining webassets
webassets = WebAssets(FileSettings(BASE_DIR=__file__, SUB_DIR="webassets"))

DEBUG = True #config("DEBUG", cast=bool, default=False)

