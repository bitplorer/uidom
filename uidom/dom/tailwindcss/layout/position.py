# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from uidom.dom.htmlelement import HTMLElement


class Static(HTMLElement):

    def render(self, elem):
        elem["class"] += " static"
        return elem


class Fixed(HTMLElement):

    def render(self, elem):
        elem["class"] += " fixed"
        return elem


class Absolute(HTMLElement):

    def render(self, elem):
        elem["class"] += " absolute"
        return elem


class Relative(HTMLElement):

    def render(self, elem):
        elem["class"] += " relative"
        return elem


class Sticky(HTMLElement):

    def render(self, elem):
        elem["class"] += " sticky"
        return elem
