# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from uidom.dom.htmlelement import HTMLElement


class Top(HTMLElement):

    def render(self, elem, sign="", position="0"):
        elem["class"] += f"{sign}top-{position}"
        return elem


class Right(HTMLElement):

    def render(self, elem, sign="", position="0"):
        elem["class"] += f"{sign}right-{position}"
        return elem


class Bottom(HTMLElement):

    def render(self, elem, sign="", position="0"):
        elem["class"] += f"{sign}bottom-{position}"
        return elem


class Left(HTMLElement):

    def render(self, elem, sign="", position="0"):
        elem["class"] += f"{sign}left-{position}"
        return elem


class Inset(HTMLElement):

    def render(self, elem, sign="", position="0"):
        elem["class"] += f"{sign}inset-{position}"
        return elem
