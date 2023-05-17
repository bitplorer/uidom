# Copyright (c) 2023 UiDOM
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from pathlib import Path

from uidom.dom import raw
from uidom.dom.src.component import Component

__all__ = ["x_component_js_text", "x_component_js"]


def x_component_js_text():
    X_COMPONENT_SCRIPT_FILE = Path(__file__).parent / "xcomponent.js"
    if not X_COMPONENT_SCRIPT_FILE.exists():
        raise FileNotFoundError(f"{X_COMPONENT_SCRIPT_FILE=} doesn't exists")
    return X_COMPONENT_SCRIPT_FILE.read_text()


class x_component_js(Component):
    file_extension = ".js"

    def render(self):
        return raw(x_component_js_text())


if __name__ == "__main__":
    print(x_component_js())
