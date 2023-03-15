# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from uidom.dom.htmlelement import HTMLElement


class OverflowAuto(HTMLElement):

    def render(self, elem):
        elem["class"] += " overflow-auto"
        return elem


class OverflowHidden(HTMLElement):

    def render(self, elem):
        elem["class"] += " overflow-hidden"
        return elem


class OverflowVisible(HTMLElement):

    def render(self, elem):
        elem["class"] += " overflow-visible"
        return elem


class OverflowScroll(HTMLElement):

    def render(self, elem):
        elem["class"] += " overflow-scroll"
        return elem


class OverflowXAuto(HTMLElement):

    def render(self, elem):
        elem["class"] += " overflow-x-auto"
        return elem


class OverflowYAuto(HTMLElement):

    def render(self, elem):
        elem["class"] += " overflow-y-auto"
        return elem


class OverflowXHidden(HTMLElement):

    def render(self, elem):
        elem["class"] += " overflow-x-hidden"
        return elem


class OverflowYHidden(HTMLElement):

    def render(self, elem):
        elem["class"] += " overflow-y-hidden"
        return elem


class OverflowXVisible(HTMLElement):

    def render(self, elem):
        elem["class"] += " overflow-x-visible"
        return elem


class OverflowYVisible(HTMLElement):

    def render(self, elem):
        elem["class"] += " overflow-y-visible"
        return elem


class OverflowXScroll(HTMLElement):

    def render(self, elem):
        elem["class"] += " overflow-x-scroll"
        return elem


class OverflowYScroll(HTMLElement):

    def render(self, elem):
        elem["class"] += " overflow-x-scroll"
        return elem
