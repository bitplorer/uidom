# Copyright (c) 2022 uidom
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from dataclasses import dataclass, field

from uidom.dom.src import component
from uidom.dom.src.dom_tag import dom_tag
from uidom.dom.src.main import extension

__all__ = ["Head", "HtmlDocument"]


class Head(component.Component):
    def render(self, *args, **kwargs):
        self.add(kwargs)
        self.add(*args)
        return self


@dataclass(eq=False)
class HtmlDocument(component.Component):
    csrf_field = "X-CSRF-TOKEN"
    ensure_csrf_token: bool = field(default=True, init=False)

    def __init__(self, *args, **kwargs):
        self.ensure_csrf_token = kwargs.pop("ensure_csrf_token", self.ensure_csrf_token)
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

    # def add(self, *args):
    #     added = super().add(*args)
    #     self._may_shift_Head_to_head()
    #     return added

    # def _may_shift_Head_to_head(self):
    #     if head_node_list := self.body.get(Head):
    #         # we expect only one Head element per Document
    #         head_node = head_node_list[0]
    #         head_parent: dom_tag = head_node.parent
    #         if head_parent.document:
    #             head_parent.remove(head_node)
    #             head_parent.document.head.add(head_node)

    def __checks__(self, element):
        if self.ensure_csrf_token:
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

        doc = self.html_tags.DocType("html")
        with self.html_tags.html() as self.html:
            # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # ^Head Section
            # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            with self.html_tags.head() as self.head:
                if any(head):
                    for _head_file in head:
                        if isinstance(_head_file, dom_tag):
                            self.head.add(_head_file)
                        elif isinstance(_head_file, str):
                            self.head.add(self.html_tags.link(href=_head_file))
                        elif isinstance(_head_file, dict):
                            self.head.add(self.html_tags.link(**_head_file))

                if any(common_head):
                    _ = [
                        self.head.add(_hd)
                        for _hd in common_head
                        if isinstance(_hd, dom_tag)
                    ]
            # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # $Head Section
            # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

            # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # ^Body Section
            # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            self._entry_with_context = extension.PlaceholderTag()
            with self.html_tags.body(
                self._entry_with_context, *args, **kwargs
            ) as self.body:
                if any(body):
                    for _body_file in body:
                        if isinstance(_body_file, dom_tag):
                            self.body.add(_body_file)
                        elif isinstance(_body_file, str):
                            self.body.add(self.html_tags.script(src=_body_file))
                        elif isinstance(_body_file, dict):
                            self.body.add(self.html_tags.script(**_body_file))

                if any(common_body):
                    _ = [
                        self.body.add(_bd)
                        for _bd in common_body
                        if isinstance(_bd, dom_tag)
                    ]
            # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # $Body Section
            # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        if not self.head.get("meta", charset="utf-8"):
            charset = self.html_tags.meta(charset="utf-8")
            self.head.add(charset)

        if not self.head.get("meta", name="viewport"):
            viewport_meta = self.html_tags.meta(
                name="viewport",
                content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, minimal-ui",
            )
            self.head.add(viewport_meta)

        return doc, self.html

    # def _render(self, sb, indent_level=1, indent_str="  ", pretty=True, xhtml=False):
    #     if self.document is None:
    #         self.setdocument(self)
    #     return super()._render(sb, indent_level, indent_str, pretty, xhtml)
