# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from uidom.dom.htmlelement import HTMLElement

__all__ = [
    "FlexColumn",
    "FlexRow"
]


class FlexColumn(HTMLElement):

    def __render__(self, elem):
        elem["class"] += " flex-col"
        return elem


class FlexRow(HTMLElement):

    def __render__(self, elem):
        elem["class"] += " flex-row"
        return elem


class FlexColumnReversed(HTMLElement):

    def __render__(self, elem):
        elem["class"] += " flex-col-reverse"
        return elem


class FlexRowReversed(HTMLElement):

    def __render__(self, elem):
        elem["class"] += " flex-row-reverse"
        return elem
