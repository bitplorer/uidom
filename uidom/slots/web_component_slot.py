# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


import typing
from dataclasses import dataclass

from uidom.dom.htmlelement import *
from uidom.dom.src.htmltags import *
from uidom.slots.custom_element_slot import x_slot

__all__ = [
    "WebComponentSlot"
]


@dataclass
class WebComponentSlot(XComponent):
    slot_names: typing.Union[list, tuple]
    classes: dict
    css: list[str]
    slot_class: str = ''

    def __post_init__(self):
        super(WebComponentSlot, self).__post_init__(
            slot_names=self.slot_names,
            classes=self.classes,
            css=self.css,
            slot_class=self.slot_class
        )

    def render(
            self,
            tag_name,
            slot_names,
            classes,
            css,
            slot_class
    ):
        return div(
            template(
                x_slot(
                    slotnames=slot_names,
                    container_part=f"{tag_name}",
                    classes=classes,
                    css=css,
                    exportparts="*",
                    className=slot_class if slot_class != '' else False,
                ), tabindex=0
            ),
            x_component=tag_name, shadowroot="true"
        )

    def __checks__(self, element):
        # XComponent.__checks__(self, element)
        # return self.__shadowroot_checks(element)
        return element

    def __call__(self, *args, **kwargs):
        return super(WebComponentSlot, self).__call__(*args, exportparts="*", **kwargs)
