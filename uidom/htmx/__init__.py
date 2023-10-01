# Copyright (c) 2023 UiDOM
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


import typing

from uidom.htmx.middleware import HtmxMiddleware
from uidom.web_io import HtmxEvents

__all__ = ["Htmx", "HtmxMiddleware"]


class Htmx(HtmxEvents):

    """
    Htmx class can be used to decorate Component class methods as follows::

        from fastapi.requests import Request
        from demosite.api import api
        from demosite.document import document
        from uidom.dom import Component

        htmx = Htmx(api=api)

        class CustomButton(Component):

            def render(self, ...):
                # The API object that will handle requests and responses

            @htmx.get
            @staticmethod
            def custom_button(request: Request):
                if request.headers.get("hx-request", None):
                    return CustomButton(...)
                return document(CustomButton(...))

        api = htmx.api

        # now import api into route module and it will be available in app
    """

    def __init__(self, api: typing.Any):
        self.api = api
        super().__init__()

    def get(self, event):
        wrapper = super(Htmx, self).get(event)
        return self.api.get(f"/{self.registered_events[-1]}")(wrapper)

    def post(self, event):
        wrapper = super(Htmx, self).post(event)
        return self.api.post(f"/{self.registered_events[-1]}")(wrapper)

    def put(self, event):
        wrapper = super(Htmx, self).put(event)
        return self.api.put(f"/{self.registered_events[-1]}")(wrapper)

    def patch(self, event):
        wrapper = super(Htmx, self).patch(event)
        return self.api.patch(f"/{self.registered_events[-1]}")(wrapper)

    def delete(self, event):
        wrapper = super(Htmx, self).delete(event)
        return self.api.delete(f"/{self.registered_events[-1]}")(wrapper)
