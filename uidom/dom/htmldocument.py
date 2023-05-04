# Copyright (c) 2022 uidom
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from dataclasses import dataclass, field

from uidom.dom import htmlelement as htm
from uidom.dom.src import dom_tag
from uidom.dom.src.main import extension

__all__ = ["HtmlDocument"]


class Meta(htm.HTMLElement):
    def render(self, **kwargs):
        return self.html_tags.meta(**kwargs)


class Head(htm.HTMLElement):
    def render(self, *args, **kwargs):
        return self.html_tags.head(*args, **kwargs)


class Body(htm.HTMLElement):
    def render(self, *args, **kwargs):
        return self.html_tags.body(*args, **kwargs)


@dataclass(eq=False)
class HtmlDocument(htm.HTMLElement):
    csrf_field = "X-CSRF-TOKEN"
    ensure_csrf_token_in_meta: bool = field(default=True, init=False)

    def __init__(self, *args, **kwargs):
        self.document = self
        super(HtmlDocument, self).__init__(*args, **kwargs)
        self._entry = self.body
        self._old_entry = None

    def __enter__(self):
        super().__enter__()
        self._old_entry = self._entry
        self._entry = self._entry_with_context
        return self

    def __exit__(self, type, value, traceback):
        super().__exit__(type, value, traceback)
        self._entry = self._old_entry

    def __checks__(self, element):
        if self.ensure_csrf_token_in_meta:
            token_element = element.get(name=self.csrf_field)
            if not token_element:
                raise AttributeError(
                    f"{self.__class__.__qualname__} {self.csrf_field} must be set"
                )
            if len(token_element) > 1:
                raise AssertionError(
                    f"{self.__class__.__qualname__} {self.csrf_field} set at multiple places"
                )
        return element

    def render(
        self, *args, head=None, body=None, common_head=None, common_body=None, **kwargs
    ):
        common_head = (
            [common_head] if not isinstance(common_head, list) else common_head
        )
        common_body = (
            [common_body] if not isinstance(common_body, list) else common_body
        )
        head = [head] if not isinstance(head, list) else head
        body = [body] if not isinstance(body, list) else body

        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # ^Head Section
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        self.head = Head()

        if any(head):
            for _head_file in head:
                if isinstance(_head_file, dom_tag):
                    self.head.add(_head_file)
                elif isinstance(_head_file, str):
                    self.head.add(self.html_tags.link(href=_head_file))
                elif isinstance(_head_file, dict):
                    self.head.add(self.html_tags.link(**_head_file))

        if any(common_head):
            _ = [self.head.add(_hd) for _hd in common_head if isinstance(_hd, dom_tag)]
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # $Head Section
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # ^Body Section
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        self._entry_with_context = extension.PlaceholderTag()
        self.body = Body(self._entry_with_context, *args, **kwargs)

        if any(body):
            for _body_file in body:
                if isinstance(_body_file, dom_tag):
                    self.body.add(_body_file)
                elif isinstance(_body_file, str):
                    self.body.add(self.html_tags.script(src=_body_file))
                elif isinstance(_body_file, dict):
                    self.body.add(self.html_tags.script(**_body_file))

        if any(common_body):
            _ = [self.body.add(_bd) for _bd in common_body if isinstance(_bd, dom_tag)]
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # $Body Section
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        if not self.head.get("meta", name="viewport"):
            viewport_meta = Meta(
                name="viewport",
                content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, minimal-ui",
            )
            self.head.add(viewport_meta)

        if not self.head.get("meta", charset="utf-8"):
            charset = Meta(charset="utf-8")
            self.head.add(charset)

        self.html = self.html_tags.html(self.head, self.body)
        doc = self.html_tags.DocType("html")
        return doc & self.html
