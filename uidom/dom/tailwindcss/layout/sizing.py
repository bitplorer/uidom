# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from uidom.dom.htmlelement import HTMLElement


class BoxBorder(HTMLElement):

    def render(self, elem):
        elem["class"] += "box-border"
        return elem


class BoxContent(HTMLElement):

    def render(self, elem):
        elem["class"] += "box-content"
        return elem
