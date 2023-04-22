# Copyright (c) 2023 UiDOM
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from typing import Any, AsyncIterator, Optional, Protocol

from uidom.web_io._types import MESSAGE, Receive, Scope, Send

__all__ = ["WebSocketProtocol"]


class WebSocketProtocol(Protocol):
    def __init__(self, scope: Scope, receive: Receive, send: Send) -> None:
        ...

    async def accept(self) -> None:
        ...

    async def close(self, code: int = 1000, reason: Optional[str] = None) -> None:
        ...

    async def receive(self) -> MESSAGE:
        ...

    async def receive_text(self) -> str:
        ...

    async def receive_bytes(self) -> bytes:
        ...

    async def receive_json(self, mode: str = "text") -> Any:
        ...

    async def send(self, message: MESSAGE) -> None:
        ...

    async def send_text(self, data: str) -> None:
        ...

    async def send_bytes(self, data: bytes) -> None:
        ...

    async def send_json(self, data: Any, mode: str = "text") -> None:
        ...

    # look at the reason below to make all iter_* method as def not async def
    # https://github.com/python/mypy/issues/5385
    def iter_text(self) -> AsyncIterator[str]:
        ...

    def iter_bytes(self) -> AsyncIterator[bytes]:
        ...

    def iter_json(self) -> AsyncIterator[Any]:
        ...

    # async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
    #     ...
