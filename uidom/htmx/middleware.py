# Copyright (c) 2023 UiDOM
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import json
from functools import cached_property
from typing import Any, Optional
from urllib.parse import unquote

from starlette.middleware.base import BaseHTTPMiddleware

__all__ = ["HtmxMiddleware"]


class HtmxDetails:
    def __init__(self, request) -> None:
        self.request = request

    def _get_header_value(self, name: str) -> Optional[str]:
        value = self.request.headers.get(name) or None
        if value:
            if self.request.headers.get(f"{name}-URI-AutoEncoded") == "true":
                value = unquote(value)
        return value

    def __bool__(self) -> bool:
        return self._get_header_value("HX-Request") == "true"

    @cached_property
    def boosted(self) -> bool:
        return self._get_header_value("HX-Boosted") == "true"

    @cached_property
    def current_url(self) -> Optional[str]:
        return self._get_header_value("HX-Current-URL")

    @cached_property
    def history_restore_request(self) -> bool:
        return self._get_header_value("HX-History-Restore-Request") == "true"

    @cached_property
    def prompt(self) -> Optional[str]:
        return self._get_header_value("HX-Prompt")

    @cached_property
    def target(self) -> Optional[str]:
        return self._get_header_value("HX-Target")

    @cached_property
    def trigger(self) -> Optional[str]:
        return self._get_header_value("HX-Trigger")

    @cached_property
    def trigger_name(self) -> Optional[str]:
        return self._get_header_value("HX-Trigger-Name")

    @cached_property
    def triggering_event(self) -> Any:
        value = self._get_header_value("Triggering-Event")
        if value is not None:
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                value = None
        return value


class HtmxMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        details = HtmxDetails(request)
        request.state.htmx: HtmxDetails = details
        return await call_next(request)
