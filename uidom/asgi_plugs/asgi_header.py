# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from functools import wraps

# Taken from https://docs.datasette.io/en/stable/plugin_hooks.html#asgi-wrapper-datasette


def asgi_wrapper(dom):
    def wrap_with_dom_header(app):
        @wraps(app)
        async def add_x_dom_header(scope, receive, send):
            async def wrapped_send(event):
                if event["type"] == "http.response.start":
                    original_headers = event.get("headers") or []
                    event = {
                        "type": event["type"],
                        "status": event["status"],
                        "headers": original_headers + [
                            [b"x-dom",
                            ", ".join(dom.attributes.keys()).encode("utf-8")]
                        ],
                    }
                await send(event)
            await app(scope, receive, wrapped_send)
        return add_x_dom_header
    return wrap_with_dom_header
