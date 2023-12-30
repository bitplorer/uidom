# Copyright (c) 2022 uidom
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


import sys
from dataclasses import dataclass
from pathlib import Path

from uidom.dom.src import component
from uidom.dom.src.ext import DoubleTags
from uidom.dom.src.jinjatags import render_jinja

__all__ = [
    "HTMLElement",
    "XTemplate",
    "AMPElement",
    "XElement",
    "CustomElement",
    "WebComponent",
    "AlpineElement",
    "AlpineComponent",
    "JinjaElement",
    "MarkdownElement",
]


@dataclass(eq=False)
class HTMLElement(component.Component):
    escape_string = False

    def __init__(self, *args, **kwargs):
        super(HTMLElement, self).__init__(*args, **kwargs)

    def __post_init__(self, *args, **kwargs):
        super(HTMLElement, self).__post_init__(*args, **kwargs)

    def render(self, elem_or_str_or_path):
        return elem_or_str_or_path

    def __and__(self, other):
        return super().__and__(other)


@dataclass(eq=False)
class AMPElement(component.Component):
    tag_name: str

    def __post_init__(self, *args, **kwargs):
        super(AMPElement, self).__init__(*args, tag_name=self.tag_name, **kwargs)

        class Element(DoubleTags):
            tagname = f"amp-{self.tag_name}"  # noqa

        self.Element = Element
        self.Element.is_inline = self.is_inline
        self.Element.is_single = self.is_single
        self.Element.is_pretty = self.is_pretty

    def __call__(self, *args, **kwargs):
        return self.Element(*args, **kwargs)

    def __and__(self, other):
        return super().__and__(other)


@dataclass(eq=False)
class XTemplate(DoubleTags):
    def __init__(self, *args, **kwargs):
        if getattr(self, "xelement", None) is None:
            parent_path = Path(sys.modules["__main__"].__file__).parent
            self.xelement = HTMLElement(parent_path / kwargs.pop("filename"))
            self.tagname = f"x-{self.xelement['x-tagname']}"
        super(XTemplate, self).__init__(*args, **kwargs)

    def __hash__(self) -> int:
        return super().__hash__()


@dataclass(eq=False)
class XElement(component.Component):
    tag_name: str

    def __post_init__(self, *args, **kwargs):
        super(XElement, self).__init__(*args, tag_name=self.tag_name, **kwargs)

        class Template(XTemplate):
            tagname = f"x-{self.tag_name}"  # noqa
            xelement = self

        self.Template = Template
        self.Template.is_inline = self.is_inline
        self.Template.is_single = self.is_single
        self.Template.is_pretty = self.is_pretty

    def __checks__(self, element):
        component.Component.__checks__(self, element)
        return self.__x_element_checks(element)

    def __x_element_checks(self, element):
        x_tagname_attr = None
        try:
            # check if "x-tagname" attribute is present in element, if it throws error raise
            # AttributeError
            x_tagname_attr = element["x-tagname"]
        except AttributeError:
            pass

        if not x_tagname_attr:
            raise AttributeError(
                f"{self.__class__.__name__}.{element.__class__.__qualname__}: must have 'x-tagname' attribute"
            )
        return element

    def __call__(self, *args, **kwargs):
        return self.Template(*args, **kwargs)

    def __and__(self, other):
        return super().__and__(other)


@dataclass(eq=False)
class CustomElement(XElement):
    # using x-tagname attribute to upgrade to the element in html to light-element

    def __checks__(self, element):
        XElement.__checks__(self, element)
        return self.__custom_element_checks(element)

    def __custom_element_checks(self, element):  # noqa
        try:
            shadow_root_attr = element["shadowroot"]
        except AttributeError:
            try:
                shadow_root_attr = element["shadowdom"]
            except AttributeError:
                shadow_root_attr = None

        if shadow_root_attr:
            raise AttributeError(
                f"{self.__class__.__name__}.{element.__class__.__qualname__}: must not have 'shadowroot' or 'shadowdom' attribute"
            )
        return element


class ExampleCustomElement(CustomElement):
    def render(self, tag_name):
        # smallest example of custom elements
        with self.html_tags.template(x_component=tag_name) as cus_elem:
            self.html_tags.div()
        return cus_elem


@dataclass(eq=False)
class WebComponent(XElement):
    # using "shadowroot" or "shadowdom" attribute to upgrade to the element in html to shadow-element

    def __checks__(self, element):
        XElement.__checks__(self, element)
        return self.__web_component_checks(element)

    def __web_component_checks(self, element):  # noqa
        try:
            shadow_root_attr = element["shadowroot"]
        except AttributeError:
            shadow_root_attr = element.get(shadowroot=None)

        if not shadow_root_attr:
            try:
                shadow_root_attr = element["shadowdom"]
            except AttributeError:
                shadow_root_attr = element.get(shadowdom=None)

        if not shadow_root_attr:
            raise AttributeError(
                f"{self.__class__.__name__}.{element.__class__.__qualname__}: must have 'shadowroot' or 'shadowdom' attribute"
            )
        return element


class ExampleWebComponent(WebComponent):
    def render(self, tag_name):
        # smallest example of a web component
        with self.html_tags.template(
            x_component=tag_name, shadowroot="true"
        ) as web_comp:
            self.html_tags.slot()
        return web_comp


@dataclass(eq=False)
class AlpineElement(component.Component):
    def __checks__(self, element):
        return self.__alpine_js_checks(element)

    def __alpine_js_checks(self, element):
        # we look for x_data=None because we exactly don't know if its value is present,
        # so we get x_data for any value by making x_data=None.
        try:
            x_data_attr = element["x-data"]
        except AttributeError:
            x_data_attr = element.get(x_data=None)

        if not x_data_attr:
            raise AttributeError(
                f"{self.__class__.__name__}.{element.__class__.__qualname__}: must have 'x-data' attribute"
            )
        return element

    def __and__(self, other):
        return super().__and__(other)


@dataclass(eq=False)
class AlpineComponent(AlpineElement, XElement):
    def __checks__(self, element):
        XElement.__checks__(self, element)
        return AlpineElement.__checks__(self, element)


class JinjaElement(component.Component):
    escape_string = False

    def render(self, elem_or_str_or_path):
        return elem_or_str_or_path

    def __call__(self, **options):
        return render_jinja(self, **options)


class MarkdownElement(component.Component):
    escape_string = False
    string_is_markdown = True

    def render(self, md_str_or_path):
        return md_str_or_path
