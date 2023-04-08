# Copyright (c) 2022 uidom
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from dataclasses import dataclass, field, make_dataclass
from typing import Optional, Union

from uidom.dom.src import DoubleTags, component
from uidom.dom.src.main import extension

__all__ = [
    "HTMLElement",
    "AMPElement",
    "XComponent",
    "CustomElement",
    "WebComponent",
    "AlpineElement",
    "AlpineComponent",
]


@dataclass
class HtmlBaseMiddleware(object):
    """
    HTMLBaseMiddleware to intercept and modify dom elements.
    """


@dataclass(eq=False)
class HTMLElement(component.Component):
    def __init__(self, *args, **kwargs):
        super(HTMLElement, self).__init__(*args, **kwargs)

    def __post_init__(self, *args, **kwargs):
        super(HTMLElement, self).__post_init__(*args, **kwargs)

    def __repr__(self):
        return str(self)

    def __and__(self, other):
        return super().__and__(other)


@dataclass(eq=False)
class AMPElement(component.Component):
    tag_name: str

    def __post_init__(self, *args, **kwargs):
        super(AMPElement, self).__init__(*args, tag_name=self.tag_name, **kwargs)

        class Element(DoubleTags):
            tagname = f"amp-{self.tag_name}"  # noqa

        element = Element

        self.Element = element
        self.Element.is_inline = self.is_inline
        self.Element.is_single = self.is_single
        self.Element.is_pretty = self.is_pretty

        # super(AMPElement, self).__post_init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self.Element(*args, **kwargs)

    def __and__(self, other):
        return super().__and__(other)


@dataclass(eq=False)
class XComponent(component.Component):
    fields: Optional[list[tuple]] = field(default=None, init=False)
    tag_name: str

    def __post_init__(self, *args, **kwargs):
        super(XComponent, self).__init__(*args, tag_name=self.tag_name, **kwargs)
        if self.fields is not None:
            element = make_dataclass(
                cls_name="".join(
                    map(lambda x: x.capitalize(), self.tag_name.split("-"))
                ),
                fields=[
                    *self.fields,
                    ("tagname", str, field(init=False, default=f"x-{self.tag_name}")),
                    (
                        "attributes",
                        dict,
                        field(init=False, default_factory=dict),
                    ),
                    (
                        "children",
                        list,
                        field(init=False, default_factory=list),
                    ),
                    (
                        "document",
                        Optional[extension.Tags],
                        field(init=False, default=None),
                    ),
                ],
                bases=(DoubleTags,),
            )
        else:

            class Element(DoubleTags):
                tagname = f"x-{self.tag_name}"  # noqa

            element = Element

        self.Element = element
        self.Element.is_inline = self.is_inline
        self.Element.is_single = self.is_single
        self.Element.is_pretty = self.is_pretty
        # self.__call__.__signature__ = inspect.signature(self.Element)
        # super(XComponent, self).__post_init__(*args, **kwargs)

    def __checks__(self, element):
        component.Component.__checks__(self, element)
        return self.__x_component_checks(element)

    def __x_component_checks(self, element):
        x_component_attr = None
        try:
            # check if "x-component" attribute is present in element, if it throws error raise
            # AttributeError
            x_component_attr = element["x-component"]
        except AttributeError:
            pass

        if not x_component_attr:
            raise AttributeError(
                f"{self.__class__.__name__}.{element.__class__.__qualname__}: must have 'x-component' attribute"
            )
        return element

    def __call__(self, *args, **kwargs):
        return self.Element(*args, **kwargs)

    def __and__(self, other):
        return super().__and__(other)


@dataclass(eq=False)
class CustomElement(XComponent):
    # using x-component attribute to upgrade to the element in html to light-element

    def __checks__(self, element):
        XComponent.__checks__(self, element)
        return self.__custom_element_checks(element)

    def __custom_element_checks(self, element):  # noqa
        shadow_root_attr = None
        try:
            shadow_root_attr = element["shadowroot"]
        except AttributeError:
            pass

        if shadow_root_attr:
            raise AttributeError(
                f"{self.__class__.__name__}.{element.__class__.__qualname__}: must not have 'shadowroot' attribute"
            )
        return element

    def render(self, tag_name):
        return self.html_tags.template(self.html_tags.div(x_component=tag_name))


@dataclass(eq=False)
class WebComponent(XComponent):
    # using "shadowroot" attribute to upgrade to the element in html to shadow-element

    def __checks__(self, element):
        XComponent.__checks__(self, element)
        return self.__web_component_checks(element)

    def __web_component_checks(self, element):  # noqa
        shadow_root_attr = None
        try:
            shadow_root_attr = element["shadowroot"]
        except AttributeError:
            pass

        if not shadow_root_attr:
            raise AttributeError(
                f"{self.__class__.__name__}.{element.__class__.__qualname__}: must have 'shadowroot' attribute"
            )
        return element

    def render(self, tag_name):
        # smallest example of a web component
        return self.html_tags.template(
            self.html_tags.div(x_component=tag_name, shadowroot="true")
        )


@dataclass(eq=False)
class AlpineElement(component.Component):
    def __checks__(self, element):
        HTMLElement.__checks__(self, element)
        return self.__alpine_js_checks(element)

    def __alpine_js_checks(self, element):
        x_data_attr = None
        try:
            x_data_attr = element["x-data"]
        except AttributeError:
            pass

        if not x_data_attr:
            raise AttributeError(
                f"{self.__class__.__name__}.{element.__class__.__qualname__}: must have 'x-data' attribute"
            )
        return element

    def render(self, *args, **kwargs):
        ...

    def __and__(self, other):
        return super().__and__(other)


@dataclass(eq=False)
class AlpineComponent(AlpineElement, XComponent):
    def __checks__(self, element):
        XComponent.__checks__(self, element)
        return AlpineElement.__checks__(self, element)


# if __name__ == '__main__':
# image = CustomElement(tag_name="img")
# print(image)
# x = image(image(image("hello")), src="http://....", alt="some image", className="h-32 w-32")
# print(x)
# # print(signature(image))
# def story(*args, **kwargs):
#     return AMPElement(tag_name="story-page")(
#         AMPElement(tag_name="story-grid-layer")(
#             AMPElement(tag_name="video")(*args, **kwargs),
#     template="fill"),
#     id="cover"
# )

# print(
#     story(
#         layout="fill",
#         src="background.mp4",
#         poster="https://images.unsplash.com/photo-1605100804763-247f67b3557e?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=870&q=80",
#         muted=None,
#         autoplay=None
#         )
#       )
