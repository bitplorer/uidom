# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from uidom.dom.htmlelement import HTMLElement


class Z0(HTMLElement):

    def __render__(self, elem):
        elem["class"] += "z-0"
        return elem


class Z10(HTMLElement):

    def __render__(self, elem):
        elem["class"] += "z-10"
        return elem


class Z20(HTMLElement):

    def __render__(self, elem):
        elem["class"] += "z-20"
        return elem


class Z30(HTMLElement):

    def __render__(self, elem):
        elem["class"] += "z-30"
        return elem


class Z40(HTMLElement):

    def __render__(self, elem):
        elem["class"] += "z-40"
        return elem


class Z50(HTMLElement):

    def __render__(self, elem):
        elem["class"] += "z-50"
        return elem


class ZAuto(HTMLElement):

    def __render__(self, elem):
        elem["class"] += "z-auto"
        return elem
