# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from uidom.dom.htmlelement import HTMLElement


class Focus(HTMLElement):

    def __render__(self, elem):
        elem["class"] = ' '.join(map(lambda cls: f" focus:{cls}"
        if any(cls) and ":" not in cls else "" if not any(cls) else cls, elem["class"].split(" ")))
        return elem


class Hover(HTMLElement):

    def __render__(self, elem):
        elem["class"] = ' '.join(map(lambda cls: f" hover:{cls}"
        if any(cls) and ":" not in cls else "" if not any(cls) else cls, elem["class"].split(" ")))
        return elem
