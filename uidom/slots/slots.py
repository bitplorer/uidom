# Copyright (c) 2023 UiDOM
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from dataclasses import dataclass, field

from uidom.dom.htmlelement import *
from uidom.dom.src.htmltags import *

__all__ = ["Slots"]


@dataclass(eq=False)
class Slots(WebComponent):
    slot_names: list[str] = field(default_factory=list)
    classes: dict = field(default_factory=dict)
    css: list[str] = field(default_factory=list)

    def __post_init__(self):
        super(Slots, self).__post_init__(
            slot_names=self.slot_names,
            classes=self.classes,
            css=self.css,
        )

    def render(self, tag_name, slot_names, classes, css):
        with template(x_component=tag_name, shadowroot="true") as slots:
            # adding css files here...
            for css_href in css:
                link(href=css_href, rel="stylesheet", type="text/css")

            with div(
                className=classes.get(tag_name, False),
                part=tag_name,
                exportparts="*",
            ):
                if any(slot_names):
                    for name in slot_names:
                        with div(
                            part=name,
                            className=classes.get(name, False),
                            exportparts="*",
                        ):
                            slot(name=name)
                else:
                    slot()

        return slots

    def __call__(self, *args, **kwargs):
        return super(Slots, self).__call__(*args, exportparts="*", **kwargs)
