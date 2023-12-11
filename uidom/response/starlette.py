# Copyright (c) 2022 uidom
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


import typing as T
from asyncio import iscoroutinefunction
from functools import wraps

from starlette.background import BackgroundTask
from starlette.responses import HTMLResponse as StarletteHTMLResponse
from starlette.responses import StreamingResponse as StarletteStreamingResponse

from uidom.dom.src import ext

__all__ = ["HTMLResponse", "html_response", "StreamingResponse", "streaming_response"]

CallableType = T.TypeVar("CallableType", bound=T.Callable[..., T.Any])


class HTMLResponse(StarletteHTMLResponse):
    media_type = "text/html"

    def __init__(
        self,
        html_content: ext.Tags,
        status_code: int = 200,
        headers: dict = None,
        media_type: str = None,
        background: BackgroundTask = None,
    ) -> None:
        super().__init__(html_content, status_code, headers, media_type, background)

    def render(self, content: T.Any) -> bytes:
        if hasattr(content, "__render__"):
            content = content.__render__()
        return super().render(content=content)


def html_response(
    endpoint: T.Optional[CallableType] = None,
) -> T.Callable[..., HTMLResponse]:
    def decorate_sync_async(endpoint):
        if iscoroutinefunction(endpoint):

            @wraps(endpoint)
            async def decorated(*args, **kwargs) -> HTMLResponse:
                content = await endpoint(*args, **kwargs)
                if isinstance(content, ext.Tags):
                    return HTMLResponse(content)
                return content

        else:

            @wraps(endpoint)
            def decorated(*args, **kwargs) -> HTMLResponse:
                content = endpoint(*args, **kwargs)
                if isinstance(content, ext.Tags):
                    return HTMLResponse(content)
                return content

        return decorated

    return decorate_sync_async(endpoint)


class StreamingResponse(StarletteStreamingResponse):
    media_type = "text/html"

    def __init__(
        self,
        html_content: ext.Tags,
        status_code: int = 200,
        headers: dict = None,
        media_type: str = None,
        background: BackgroundTask = None,
    ) -> None:
        super().__init__(
            html_content.__async_render__(),
            status_code,
            headers,
            media_type,
            background,
        )


def streaming_response(
    endpoint: T.Optional[CallableType] = None,
) -> T.Callable[..., StreamingResponse]:
    def decorate_sync_async(endpoint):
        if iscoroutinefunction(endpoint):

            @wraps(endpoint)
            async def decorated(*args, **kwargs) -> StreamingResponse:
                content = await endpoint(*args, **kwargs)
                if isinstance(content, ext.Tags):
                    return StreamingResponse(content)
                return content

        else:

            @wraps(endpoint)
            def decorated(*args, **kwargs) -> StreamingResponse:
                content = endpoint(*args, **kwargs)
                if isinstance(content, ext.Tags):
                    return StreamingResponse(content)
                return content

        return decorated

    return decorate_sync_async(endpoint)
