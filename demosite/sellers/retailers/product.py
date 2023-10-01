# Copyright (c) 2023 UiDOM
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from fastapi.requests import Request

from demosite.document import document
from uidom.dom import Component, div


class Product(Component):
    def render(self, request: Request):
        res = div(
            f"Hello from {request.url}",
            className="flex bg-rose-400 h-screen",
            hx_get="/product",
        )
        if request.state.htmx:
            return res
        return document(res)
