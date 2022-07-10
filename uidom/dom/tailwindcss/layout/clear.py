# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from uidom.dom.htmlelement import HTMLElement


class ClearLeft(HTMLElement):

    def __render__(self, elem):
        elem["class"] += "clear-left"
        return elem


class ClearRight(HTMLElement):

    def __render__(self, elem):
        elem["class"] = "clear-right"
        return elem


class ClearBoth(HTMLElement):

    def __render__(self, elem):
        elem["class"] += "clear-both"
        return elem


class ClearNone(HTMLElement):

    def __render__(self, elem):
        elem["class"] += "clear-none"
        return elem
