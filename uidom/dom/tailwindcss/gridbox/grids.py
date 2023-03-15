# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from valio import Validator

from uidom.dom.htmlelement import HTMLElement


class Grid(HTMLElement):

    def render(self, elem):
        elem["class"] += " grid"
        return elem


class Columns(HTMLElement):

    def render(self, elem, columns):
        elem["class"] += f" grid-cols-{columns}"
        return elem


class ColumnAuto(HTMLElement):

    def render(self, elem):
        elem["class"] += " col-auto"
        return elem


class ColumnStart(HTMLElement):

    def render(self, elem, start="auto"):
        elem["class"] += f" col-start-{start}"
        return elem


class ColumnSpan(HTMLElement):

    def render(self, elem, span="full"):
        elem["class"] += f" col-span-{span}"
        return elem


class ColumnEnd(HTMLElement):

    def render(self, elem, end="auto"):
        elem["class"] += f" col-end-{end}"
        return elem


class Rows(HTMLElement):

    def render(self, elem, rows="none"):
        elem["class"] += f" grid-rows-{rows}"
        return elem


class RowAuto(HTMLElement):

    def render(self, elem):
        elem["class"] += f" row-auto"
        return elem


class RowStart(HTMLElement):

    def render(self, elem, start="auto"):
        elem["class"] += f" row-start-{start}"
        return elem


class RowSpan(HTMLElement):

    def render(self, elem, span="full"):
        elem["class"] += f" row-span-{span}"
        return elem


class RowEnd(HTMLElement):

    def render(self, elem, end="auto"):
        elem["class"] += f" row-span-{end}"
        return elem


class GridFlow(HTMLElement):
    flow: str = Validator(logger=False, debug=True, in_choice=["row", "col", "row-dense", "col-dense"])

    def render(self, elem, flow="row"):
        self.flow = flow
        elem["class"] += f" grid-flow-{flow}"
        return elem


class GridAutoColumn(HTMLElement):
    auto_col: str = Validator(logger=False, debug=True, in_choice=["auto", "min", "max", "fr"])

    def render(self, elem, auto_col="auto"):
        self.auto_col = auto_col
        elem["class"] += f" auto-cols-{auto_col}"
        return elem


class GridAutoRow(HTMLElement):
    auto_row: str = Validator(logger=False, debug=True, in_choice=["auto", "min", "max", "fr"])

    def render(self, elem, auto_row="auto"):
        self.auto_row = auto_row
        elem["class"] += f" auto-cols-{auto_row}"
        return elem
