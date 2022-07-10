# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from uidom.dom.htmlelement import HTMLElement


class DecorationSlice(HTMLElement):

    def __render__(self, elem):
        elem["class"] += " decoration-slice"
        return elem


class DecorationClone(HTMLElement):

    def __render__(self, elem):
        elem["class"] += " decoration-clone"
        return elem
