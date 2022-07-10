# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from uidom.dom.htmlelement import HTMLElement
from uidom.dom.tailwindcss import (Columns, Flex, FlexColumn, FlexRow,
                                        Grid, Rows)


class GridRowsColumnsDiv(HTMLElement):

    def __render__(self, *args, columns, rows, **kwargs):
        elem = self.html_tags.div(*args, **kwargs)
        elem["class"] = ""
        return Rows(Columns(Grid(elem), columns=columns), rows=rows)


class FlexColumnDiv(HTMLElement):

    def __render__(self, *args, **kwargs):
        elem = self.html_tags.div(*args, **kwargs)
        elem["class"] = ""
        return Flex(FlexColumn(elem))


class FlexRowDiv(HTMLElement):

    def __render__(self, *args, **kwargs):
        elem = self.html_tags.div(*args, **kwargs)
        elem["class"] = ""
        return FlexRow(Flex(elem))


if __name__ == '__main__':
    print(FlexRowDiv("hello world"))
