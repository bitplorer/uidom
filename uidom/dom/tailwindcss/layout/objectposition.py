# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from uidom.dom.htmlelement import HTMLElement


class ObjectBottom(HTMLElement):

    def __render__(self, elem):
        elem["class"] += "object-bottom"
        return elem


class ObjectCenter(HTMLElement):

    def __render__(self, elem):
        elem["class"] += "object-center"
        return elem


class ObjectLeft(HTMLElement):

    def __render__(self, elem):
        elem["class"] += "object-left"
        return elem


class ObjectLeftBottom(HTMLElement):

    def __render__(self, elem):
        elem["class"] += "object-left-bottom"
        return elem


class ObjectLeftTop(HTMLElement):

    def __render__(self, elem):
        elem["class"] += "object-left-top"
        return elem


class ObjectRight(HTMLElement):

    def __render__(self, elem):
        elem["class"] += "object-right"
        return elem


class ObjectRightBottom(HTMLElement):

    def __render__(self, elem):
        elem["class"] += "object-right-bottom"
        return elem


class ObjectRightTop(HTMLElement):

    def __render__(self, elem):
        elem["class"] += "object-right-top"
        return elem


class ObjectTop(HTMLElement):

    def __render__(self, elem):
        elem["class"] += "object-top"
        return elem
