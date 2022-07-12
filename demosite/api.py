# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from demosite.document import document

api = FastAPI(debug=True)
if document.webassets is not None:
    api.mount(
        "/css",
        StaticFiles(directory=document.webassets.static.css, check_dir=False),
        name="css",
    )
    api.mount(
        "/js",
        StaticFiles(directory=document.webassets.static.js, check_dir=False),
        name="js",
    )
    api.mount(
        "/image",
        StaticFiles(directory=document.webassets.static.images, check_dir=False),
        name="image",
    )
