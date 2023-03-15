# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from uidom.dom.htmlelement import HTMLElement


class OverScrollAuto(HTMLElement):

    def render(self, elem):
        elem["class"] += "overscroll-auto"
        return elem


class OverScrollContain(HTMLElement):

    def render(self, elem):
        elem["class"] += "overscroll-contain"
        return elem


class OverScrollNone(HTMLElement):

    def render(self, elem):
        elem["class"] += "overscroll-none"
        return elem


class OverScrollYAuto(HTMLElement):

    def render(self, elem):
        elem["class"] += "overscroll-y-auto"
        return elem


class OverScrollYContain(HTMLElement):

    def render(self, elem):
        elem["class"] += "overscroll-y-contain"
        return elem


class OverScrollYNone(HTMLElement):

    def render(self, elem):
        elem["class"] += "overscroll-y-none"
        return elem


class OverScrollXAuto(HTMLElement):

    def render(self, elem):
        elem["class"] += "overscroll-x-auto"
        return elem


class OverScrollXContain(HTMLElement):

    def render(self, elem):
        elem["class"] += "overscroll-x-contain"
        return elem


class OverScrollXNone(HTMLElement):

    def render(self, elem):
        elem["class"] += "overscroll-x-none"
        return elem
