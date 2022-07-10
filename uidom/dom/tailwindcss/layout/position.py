# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from uidom.dom.htmlelement import HTMLElement


class Static(HTMLElement):

    def __render__(self, elem):
        elem["class"] += " static"
        return elem


class Fixed(HTMLElement):

    def __render__(self, elem):
        elem["class"] += " fixed"
        return elem


class Absolute(HTMLElement):

    def __render__(self, elem):
        elem["class"] += " absolute"
        return elem


class Relative(HTMLElement):

    def __render__(self, elem):
        elem["class"] += " relative"
        return elem


class Sticky(HTMLElement):

    def __render__(self, elem):
        elem["class"] += " sticky"
        return elem
