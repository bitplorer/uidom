# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from uidom.dom.htmlelement import HTMLElement


class Isolate(HTMLElement):

    def __render__(self, elem):
        elem["class"] += "isolate"
        return elem


class IsolateAuto(HTMLElement):

    def __render__(self, elem):
        elem["class"] += "isolate-auto"
        return elem
