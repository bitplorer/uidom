# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from uidom.dom.htmlelement import HTMLElement


class FlexWrap(HTMLElement):

    def __render__(self, elem):
        elem["class"] += "flex-wrap"
        return elem


class FlexNoWrap(HTMLElement):

    def __render__(self, elem):
        elem["class"] += "flex-nowrap"
        return elem


class FlexWrapReverse(HTMLElement):

    def __render__(self, elem):
        elem["class"] += "flex-wrap-reverse"
        return elem
