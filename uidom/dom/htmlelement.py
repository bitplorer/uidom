# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from dataclasses import dataclass, field, make_dataclass
from typing import Union

from uidom.dom.src import DoubleTags, component

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
    file_extension = ".html"

    def __init__(self, *args, **kwargs):
        super(HTMLElement, self).__init__(*args, **kwargs)

    def __render__(self, *args, **kwargs):
        return self.html_tags.ConcatTag(*args, **kwargs)

    def __script__(self, *args, **kwargs):
        ...

    def __repr__(self):
        return str(self)


@dataclass(eq=False)
class AMPElement(HTMLElement):
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

    def __call__(self, *args, **kwargs):
        return self.Element(*args, **kwargs)


# here init=False is necessary to avoid double initialization
@dataclass(init=False, eq=False)
class XComponent(HTMLElement):
    fields = None
    tag_name: str

    def __post_init__(self, *args, **kwargs):
        super(XComponent, self).__init__(*args, tag_name=self.tag_name, **kwargs)
        if self.fields is not None:
            element = make_dataclass(cls_name=''.join(map(lambda x: x.capitalize(), self.tag_name.split('-'))),
                                     fields=[*self.fields,
                                             ("tagname", str, field(init=False, default=f"x-{self.tag_name}")),
                                             ("attributes", dict, field(init=False, default_factory=lambda: dict())),
                                             ("children", list, field(init=False, default_factory=lambda: list())),
                                             ("document", list, field(init=False, default_factory=lambda: None)),
                                             ],
                                     bases=(DoubleTags,), )
        else:
            class Element(DoubleTags):
                tagname = f"x-{self.tag_name}"  # noqa

            element = Element

        self.Element = element
        self.Element.is_inline = self.is_inline
        self.Element.is_single = self.is_single
        self.Element.is_pretty = self.is_pretty
        # self.__call__ = element.__init__

    def __checks__(self, element):
        HTMLElement.__checks__(self, element)
        return self.__x_component_checks(element)

    def __x_component_checks(self, element):
        if not element.attributes.get("x-component"):
            if not element.get(x_component=self.tag_name):
                raise AttributeError(f"{element.__class__.__qualname__}: must have 'x_component' attribute")
        return super(HTMLElement, self).__checks__(element)

    def __call__(self, *args, **kwargs):
        return self.Element(*args, **kwargs)


@dataclass(eq=False)
class CustomElement(XComponent):
    # using x-component attribute to upgrade to the element in html to light-element

    def __checks__(self, element):
        XComponent.__checks__(self, element)
        return self.__custom_element_checks(element)

    def __custom_element_checks(self, element):  # noqa
        if (element.attributes.get("shadowroot") or element.get(shadowroot="shadowroot") or element.get(
                shadowroot="true")):
            raise AttributeError(f"{element.__class__.__qualname__}: must not have 'shadowroot' attribute")
        return element

    def __render__(self, tag_name):
        return self.html_tags.template(self.html_tags.div(x_component=tag_name))


@dataclass(eq=False)
class WebComponent(XComponent):
    # using x-component attribute to upgrade to the element in html to shadow-element

    def __checks__(self, element):
        XComponent.__checks__(self, element)
        return self.__web_component_checks(element)

    def __web_component_checks(self, element):  # noqa
        if not (element.attributes.get("shadowroot") or element.get(shadowroot="shadowroot") or element.get(
                shadowroot="true")):
            raise AttributeError(f"{element.__class__.__qualname__}: must have 'shadowroot' attribute set")
        return element

    def __render__(self, tag_name):
        # smallest example of a web component
        return self.html_tags.template(self.html_tags.div(x_component=tag_name, shadowroot="true"))


@dataclass(eq=False)
class AlpineElement(HTMLElement):
    x_data: Union[str, dict, bool, None] = False

    def __checks__(self, element):
        HTMLElement.__checks__(self, element)
        return self.__alpine_js_checks(element)

    def __alpine_js_checks(self, element):
        if not self.x_data:
            x_data = element.attributes.get("x-data") or element.get(x_data=self.x_data)
            if not x_data or x_data == "False":
                raise AttributeError(f"{element.__class__.__qualname__}: must have 'x-data' attribute")
        return element

    def __render__(self, *args, **kwargs):
        ...


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
