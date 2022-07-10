# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from uidom.dom.htmlelement import HTMLElement


class FlexShrink(HTMLElement):

    def __render__(self,  elem):
        elem["class"] += "flex-shrink"
        return elem


class FlexShrink0(HTMLElement):

    def __render__(self,  elem):
        elem["class"] += "flex-shrink-0"
        return elem
