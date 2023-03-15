# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from uidom.dom.htmlelement import HTMLElement


class Container(HTMLElement):

    def render(self, elem):
        elem["class"] += " container"
        return elem


class Small(HTMLElement):

    def render(self, elem):
        elem["class"] = ' '.join(map(lambda cls: f" sm:{cls}"
        if any(cls) and ":" not in cls else "" if not any(cls) else cls, elem["class"].split(" ")))
        return elem


class Medium(HTMLElement):

    def render(self, elem):
        elem["class"] = ' '.join(map(lambda cls: f" md:{cls}"
        if any(cls) and ":" not in cls else "" if not any(cls) else cls, elem["class"].split(" ")))
        return elem


class Large(HTMLElement):

    def render(self, elem):
        elem["class"] = ' '.join(map(lambda cls: f" lg:{cls}"
        if any(cls) and ":" not in cls else "" if not any(cls) else cls, elem["class"].split(" ")))
        return elem
