# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from uidom.dom.htmlelement import HTMLElement


class Flex(HTMLElement):

    def render(self, elem):
        elem["class"] += " flex"
        return elem


class Flex1(HTMLElement):

    def render(self, elem):
        elem["class"] += " flex-1"
        return elem


class FlexAuto(HTMLElement):

    def render(self, elem):
        elem["class"] += " flex-auto"
        return elem


class FlexInitial(HTMLElement):

    def render(self, elem):
        elem["class"] += " flex-initial"
        return elem


class FlexNone(HTMLElement):

    def render(self, elem):
        elem["class"] += " flex-none"
        return elem

