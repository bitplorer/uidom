# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from uidom.dom.htmlelement import HTMLElement


class Block(HTMLElement):

    def __render__(self, elem):
        elem["class"] += " block"
        return elem


class InlineBlock(HTMLElement):

    def __render__(self, elem):
        elem["class"] += " inline-block"
        return elem


class Inline(HTMLElement):

    def __render__(self, elem):
        elem["class"] += " inline"
        return elem


class InlineFlex(HTMLElement):

    def __render__(self, elem):
        elem["class"] += " inline-flex"
        return elem


class Table(HTMLElement):

    def __render__(self, elem):
        elem["class"] += " table"
        return elem


class InlineTable(HTMLElement):

    def __render__(self, elem):
        elem["class"] += " inline-table"
        return elem


class TableCaption(HTMLElement):

    def __render__(self, elem):
        elem["class"] += " table-caption"
        return elem


class TableCell(HTMLElement):

    def __render__(self, elem):
        elem["class"] += " table-cell"
        return elem


class TableColumn(HTMLElement):

    def __render__(self, elem):
        elem["class"] += " table-column"
        return elem


class TableColumnGroup(HTMLElement):

    def __render__(self, elem):
        elem["class"] += " table-column-group"
        return elem


class TableHeaderGroup(HTMLElement):

    def __render__(self, elem):
        elem["class"] += " table-header-group"
        return elem


class TableFooterGroup(HTMLElement):

    def __render__(self, elem):
        elem["class"] += " table-header-group"
        return elem


class TableRowGroup(HTMLElement):

    def __render__(self, elem):
        elem["class"] += " table-row-group"
        return elem


class TableRow(HTMLElement):

    def __render__(self, elem):
        elem["class"] += " table-row"
        return elem


class FlowRoot(HTMLElement):

    def __render__(self, elem):
        elem["class"] += " flow-root"
        return elem


class InlineGrid(HTMLElement):

    def __render__(self, elem):
        elem["class"] += " inline-grid"
        return elem


class Contents(HTMLElement):

    def __render__(self, elem):
        elem["class"] += " contents"
        return elem


class ListItem(HTMLElement):

    def __render__(self, elem):
        elem["class"] += " list-item"
        return elem


class Hidden(HTMLElement):

    def __render__(self, elem):
        elem["class"] += " hidden"
        return elem

