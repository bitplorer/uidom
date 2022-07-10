# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


import typing
from functools import wraps

try:
    from starlette.background import BackgroundTask
    from starlette.responses import Response
except ImportError:
    BackgroundTask = None
    Response = None

__all__ = [
    "DocumentResponse",
    "doc_response"
]

F = typing.TypeVar("F", bound=typing.Callable[..., typing.Any])


class DocumentResponse(Response):
    media_type = "text/html"

    def __init__(
        self,
        html: typing.Any,
        status_code: int = 200,
        headers: dict = None,
        media_type: str = None,
        background: BackgroundTask = None,
    ):
        self.html = html
        super().__init__(self.html, status_code, headers, media_type, background)

    def render(self, content: typing.Any) -> bytes:
        if hasattr(content, "render"):
            content = content.render()
        content = super().render(content=content)
        return content


def doc_response(html_doc: F) -> F:
    @wraps(html_doc)
    def decorator(*args, **kwargs) -> DocumentResponse:
        return DocumentResponse(html_doc(*args, **kwargs))
    return decorator
