# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from uidom.dom.htmlelement import HTMLElement


class Visible(HTMLElement):

    def __render__(self, elem):
        elem["class"] += "visible"
        return elem


class Invisible(HTMLElement):

    def __render__(self, elem):
        elem["class"] += "invisible"
        return elem
