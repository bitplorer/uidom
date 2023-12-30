# Copyright (c) 2023 UiDOM
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from pathlib import Path

from uidom.dom import raw
from uidom.dom.src.component import Component

__all__ = ["x_component_js", "custom_element_js"]


def read_text(file_name):
    SCRIPT_FILE = Path(__file__).parent / file_name
    if not SCRIPT_FILE.exists():
        raise FileNotFoundError(f"{SCRIPT_FILE=} doesn't exists")
    return SCRIPT_FILE.read_text()


class x_component_js(Component):
    file_extension = ".js"

    def render(self):
        return raw(read_text("xcomponent.js"))


class html_elements(Component):
    file_extension = ".js"

    def render(self):
        return raw(read_text("html_element.js"))
