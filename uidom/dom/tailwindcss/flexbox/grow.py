# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from uidom.dom.htmlelement import HTMLElement


class FlexGrow(HTMLElement):

    def __render__(self, elem):
        elem["class"] += " flex-grow"
        return elem


class FlexGrow0(HTMLElement):

    def __render__(self, elem):
        elem["class"] += " flex-grow-0"
        return elem
