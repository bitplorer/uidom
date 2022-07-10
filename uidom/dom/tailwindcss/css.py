# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from functools import wraps

from .flexbox import Flex, FlexColumn, FlexRow
from .gridbox import (ColumnEnd, Columns, ColumnSpan, ColumnStart, Grid,
                      GridFlow, RowEnd, Rows, RowSpan, RowStart)
from .layout import Large, Medium, Small
from .responsive import Focus, Hover


def flex(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return Flex(func(*args, **kwargs))
    return wrapper


def flex_col(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return FlexColumn(func(*args, **kwargs))
    return wrapper


def flex_row(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return FlexRow(func(*args, **kwargs))
    return wrapper


def grid(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return Grid(func(*args, **kwargs))
    return wrapper


def grid_flow(flow="row"):
    def fn(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return GridFlow(func(*args, **kwargs), flow=flow)
        return wrapper
    return fn


def hover(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return Hover(func(*args, **kwargs))
    return wrapper


def focus(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return Focus(func(*args, **kwargs))
    return wrapper


def sm(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return Small(func(*args, **kwargs))
    return wrapper


def md(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return Medium(func(*args, **kwargs))
    return wrapper


def lg(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return Large(func(*args, **kwargs))
    return wrapper


def column(columns="12"):
    def fn(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return Columns(func(*args, **kwargs), columns=columns)
        return wrapper
    return fn


def column_start(start="1"):
    def fn(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return ColumnStart(func(*args, **kwargs), start=start)
        return wrapper
    return fn


def column_span(span="1"):
    def fn(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return ColumnSpan(func(*args, **kwargs), span=span)
        return wrapper
    return fn


def column_end(end="1"):
    def fn(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return ColumnEnd(func(*args, **kwargs), end=end)
        return wrapper
    return fn


def row(rows="6"):
    def fn(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return Rows(func(*args, **kwargs), rows=rows)
        return wrapper
    return fn


def row_start(start="1"):
    def fn(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return RowStart(func(*args, **kwargs), start=start)
        return wrapper
    return fn


def row_span(span="1"):
    def fn(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return RowSpan(func(*args, **kwargs), span=span)
        return wrapper
    return fn


def row_end(end="1"):
    def fn(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return RowEnd(func(*args, **kwargs), end=end)
        return wrapper
    return fn
