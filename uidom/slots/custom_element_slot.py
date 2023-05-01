# Copyright (c) 2022 uidom
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from dataclasses import dataclass, field

from uidom.dom.htmlelement import *
from uidom.dom.src.htmltags import *

__all__ = ["SlotElement", "x_slot"]


@dataclass
class SlotElement(CustomElement):
    def render(self, tag_name):
        """
        :param tag_name:
        :return:
        """
        return template(
            div(
                template(
                    link(x_bind_href="ss", rel="stylesheet", type="text/css"),
                    x_for="ss in css",
                ),
                template(
                    div(
                        slot(x_bind_name="name"),
                        x_bind_part="name",
                        x_bind_class="classes[name]",
                        exportparts="*",
                    ),
                    x_for="name in slotnames",
                    tabindex=0,
                    x_if=" !!slotnames && slotnames.length && slotnames[0] !== '' ",
                ),
                template(
                    slot(),
                    tabindex=0,
                    x_if=" !slotnames || !slotnames.length || (slotnames.length && slotnames[0] == '') ",
                ),
                x_bind_class="classes[`${container_part}`]",
                x_bind_part="container_part",
                exportparts="*",
                x_data="{...slots(), ...$el.parentElement.data()}",
                x_cloak=None,
            ),
            script(
                """function slots(){
                return {
                    slotnames: [''],
                    classes:{}, 
                    css:[''] , 
                    container_part: ''
                        }
                    }"""
            ),
            x_component=tag_name,
        )


x_slot = SlotElement(tag_name="slot")

if __name__ == "__main__":
    print(x_slot.get(x_data=None))
