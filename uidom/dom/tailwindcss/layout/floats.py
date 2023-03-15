# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from uidom.dom.htmlelement import HTMLElement


class FloatRight(HTMLElement):

    def render(self, elem):
        elem["class"] += "float-right"
        return elem


class FloatLeft(HTMLElement):

    def render(self, elem):
        elem["class"] += "float-left"
        return elem


class FloatNone(HTMLElement):

    def render(self, elem):
        elem["class"] += "float-none"
        return elem
