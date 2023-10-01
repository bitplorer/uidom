# Copyright (c) 2022 uidom
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


import builtins
import os
import sys
import types
import typing as T
from copy import deepcopy
from dataclasses import dataclass, field

from uidom.dom.src import ext, htmltags, jinjatags, svgtags
from uidom.dom.src.htmltags import html_tag
from uidom.dom.src.parse_html import Element, tokenize_html
from uidom.dom.src.utils import dom_text

__all__ = ["StringToHTML", "defHTML"]


def create_dynamic_element(tag_name: str) -> T.Type[ext.Tags]:
    class _Element(ext.Tags):
        tagname = tag_name

    cls_name = "".join(map(lambda x: x.capitalize(), tag_name.split("-")))
    _Element.__qualname__ = cls_name
    _Element.__name__ = cls_name
    module_name: str = os.path.splitext(os.path.basename(sys.modules["__main__"].__file__))[0]  # type: ignore
    _Element.__module__ = module_name
    element: T.Type[ext.Tags] = deepcopy(_Element)
    del _Element
    setattr(sys.modules["__main__"], cls_name, element)
    return element


@dataclass
class StringToHTML(object):
    # TODO convert DOM object instance to Code Object for AST conversion to python code.
    # from https://stackoverflow.com/questions/68577587/how-to-find-the-ast-assignment-node-related-to-the-instance-creation
    # this.ast_object can be easily used to create python code for any html object
    # https://stackoverflow.com/a/68584740 for parsing a python object into an ast_object
    # https://stackoverflow.com/a/63212256 for unparsing a python ast_object

    html_string_or_token: T.Union[str, Element, list[Element], ext.Tags]
    modules: list[types.ModuleType] = field(default_factory=list)
    escape: bool = field(default=True)

    def __post_init__(self):
        self.tokens: T.Union[Element, list[Element], ext.Tags] = (
            tokenize_html(
                self.html_string_or_token
                if not isinstance(self.html_string_or_token, html_tag)
                else str(self.html_string_or_token)
            ).children
            if isinstance(self.html_string_or_token, (str, html_tag))
            else self.html_string_or_token
        )

        # for html, svg and jinja tags lookup
        if htmltags not in self.modules:
            self.modules.append(htmltags)

        if svgtags not in self.modules:
            self.modules.append(svgtags)

        if jinjatags not in self.modules:
            self.modules.append(jinjatags)

    def parse(self, tag: T.Optional[ext.Tags] = None) -> T.Union[str, ext.Tags, None]:
        for token in self.tokens:
            if not token.name:
                # myst_parser gives out Data['abc'] kind of Token with {"name":'', 'data': 'abc', ...} attributes
                # we are parsing plain strings, <script> body or jinja token strings here

                if hasattr(token, "data"):
                    # handle leading and trailing newline with spaces in myst parser Data Token ex: "  \n Hello\n  "
                    if data := token.data.strip("\n").strip(" ").strip("\n"):
                        with tag or ext.PlaceholderTag() as tag:
                            # handling
                            if tag.__class__.__name__ == "script":
                                dom_text(data, escape=False)
                            else:
                                if token.__class__.__name__ != "Comment":
                                    if data.startswith("{") and data.endswith("}"):
                                        # these are jinja tags
                                        dom_text(data, escape=False)
                                    else:
                                        # normal text is here
                                        dom_text(data, escape=self.escape)
                                else:
                                    # this is a comment section
                                    htmltags.comment(data)

            else:
                element = None
                tag_name = token.name
                if tag_name in builtins.__dict__:
                    # work around for builtins like 'input' tag
                    tag_name = "".join([token.name, "_"])

                for module in self.modules:
                    try:
                        element = getattr(module, tag_name)
                        if element is not None:
                            break
                    except (AttributeError,):
                        pass
                if element is None:
                    element = create_dynamic_element(tag_name=tag_name)

                # tag = tag if tag is not None else ConcatTag()

                if tag is not None:
                    with tag:
                        with element(**token.attrs) as child_tag:
                            StringToHTML(
                                token.children, modules=self.modules, escape=self.escape
                            ).parse(tag=child_tag)
                else:
                    with element(**token.attrs) as tag:
                        StringToHTML(
                            token.children, modules=self.modules, escape=self.escape
                        ).parse(tag=tag)
        return tag

    def __repr__(self):
        return str(self.parse())


# don't decorate defHTML with functools.lru_cache because if defHTML is used in isolation
# like:
# with div() as parent_div:
#   child_element = defHTML("some html string")
#
# with lru_cache decorated on defHTML the evaluation of child_element at run time will not happen twice
# and thus parent_div will never add child_element in subsequest runs thus better way to cache defHTML
# evaluation is to cache the method where it is used.
def defHTML(raw_string, escape=True) -> T.List[ext.Tags]:  # noqa
    tokens = tokenize_html(raw_string).children
    elements = []
    for token in tokens:
        element = StringToHTML([token], escape=escape).parse()
        if element:
            assert isinstance(
                element, ext.Tags
            ), f"{element=} is not instance of {ext.Tags}"
            elements.append(element)
    return elements


# if __name__ == '__main__':
# from uidom.dom import ConcatTag, For, Var, div, li, raw, script, ul

# print(defHTML("<li><ul><i><!--Hello World--></i></ul><a href='www.google.com'></a></li>"))
#     class XName(ext.Tags):
#         tagname = "x-name"


# print(defHTML(div("hello", div("Jai SHree Ram"), script(raw("function () => {}")), className="sdaf")).parse())
# print(div("hello", div("Jai SHree Ram"), script(raw("function () => {}")), className="sdaf"))
# print(defHTML(str(div("hello", div("Jai SHree Ram"), script(raw("function () => {}")), className="sdaf", x_data=None))))
# x = HTMLToPy(str(XName("hello", Var("haha"), ul(For("name in names", li(Var("name")))),
#                        div("Jai SHree Ram aa", className="safn"), script(raw("function () => {}")),
#                         script(src="https://unpkg.com/filepond/dist/filepond.js"),
#                         className="sdaf", x_data={}, x_transition_enter="")))
# print(x)
# print(XName("hello >", Var("haha >"), ul(For("name in names", li(Var("name")))),
#             div("Jai SHree Ram   a ", className="safn"), script(raw("function () => {}")),
#                         script(src="https://unpkg.com/filepond/dist/filepond.js"),
#                         className="sdaf", x_data={}, x_transition_enter=""))
# print(defHTML(str(ul(For("name in names", li(Var("name")))))))
