# Copyright (c) 2023 UiDOM
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from functools import lru_cache
from pathlib import Path

from uidom.dom import raw, script

__all__ = ["x_component_js_text"]

X_COMPONENT_SCRIPT_FILE = Path(__file__).parent / "xcomponent.js"
assert X_COMPONENT_SCRIPT_FILE.exists()


@lru_cache
def x_component_js_text():
    return X_COMPONENT_SCRIPT_FILE.read_text()


if __name__ == "__main__":
    print(x_component_js_text)
