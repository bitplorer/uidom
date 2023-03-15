# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from uidom.dom.htmlelement import HTMLElement


class ObjectContain(HTMLElement):

    def render(self, elem):
        elem["class"] += " object-contain"
        return elem


class ObjectCover(HTMLElement):

    def render(self, elem):
        elem["class"] += " object-cover"
        return elem


class ObjectFill(HTMLElement):

    def render(self, elem):
        elem["class"] += " object-fill"
        return elem


class ObjectNone(HTMLElement):

    def render(self, elem):
        elem["class"] += " object-none"
        return elem


class ObjectScaleDown(HTMLElement):

    def render(self, elem):
        elem["class"] += " object-scale-down"
        return elem
