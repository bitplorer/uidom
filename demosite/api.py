# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


try:
    from fastapi import FastAPI
    from fastapi.staticfiles import StaticFiles
except ImportError:
    FastAPI, StaticFiles = None, None
    
from demosite.dom import document

if FastAPI is not None:
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

else:
    api = None 
