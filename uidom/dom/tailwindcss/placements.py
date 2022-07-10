# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from uidom.dom.htmlelement import HTMLElement
from valio import Validator


class Gap(HTMLElement):

    def __render__(self, elem, gap=""):
        elem["class"] += f" gap-{gap}"
        return elem


class GapX(HTMLElement):

    def __render__(self, elem, x="px"):
        elem["class"] += f" gap-x-{x}"
        return elem


class GapY(HTMLElement):

    def __render__(self, elem, y="px"):
        elem["class"] += f" gap-y-{y}"
        return elem


class JustifyContent(HTMLElement):
    justify: str = Validator(logger=False,
                             debug=True,
                             in_choice=["start", "end", "center", "between", "around", "evenly"])

    def __render__(self, elem, justify="center"):
        self.justify = justify
        elem["class"] += f" justify-{justify}"
        return elem


class JustifyItem(HTMLElement):
    justify: str = Validator(logger=False,
                             debug=True,
                             in_choice=["start", "end", "center", "stretch"])

    def __render__(self, elem, justify="center"):
        self.justify = justify
        elem["class"] += f" justify-items-{justify}"
        return elem


class JustifySelf(HTMLElement):
    justify: str = Validator(logger=False,
                             debug=True,
                             in_choice=["start", "end", "center", "stretch", "auto"])

    def __render__(self, elem, justify="center"):
        self.justify = justify
        elem["class"] += f" justify-self-{justify}"
        return elem


class AlignContent(HTMLElement):
    align: str = Validator(logger=False,
                           debug=True,
                           in_choice=["start", "end", "center", "between", "around", "evenly"])

    def __render__(self, elem, align="center"):
        self.align = align
        elem["class"] += f" content-{align}"
        return elem


class AlignItem(HTMLElement):
    align: str = Validator(logger=False,
                           debug=True,
                           in_choice=["start", "end", "center", "stretch", "baseline"])

    def __render__(self, elem, align="center"):
        self.align = align
        elem["class"] += f" items-{align}"
        return elem


class AlignSelf(HTMLElement):
    align: str = Validator(logger=False,
                           debug=True,
                           in_choice=["start", "end", "center", "stretch", "auto"])

    def __render__(self, elem, align="center"):
        self.align = align
        elem["class"] += f" self-{align}"
        return elem


class PlaceContent(HTMLElement):
    place: str = Validator(logger=False,
                           debug=True,
                           in_choice=["start", "end", "center", "between", "around", "evenly", "stretch"])

    def __render__(self, elem, place="center"):
        self.place = place
        elem["class"] += f" place-content-{place}"
        return elem


class PlaceItem(HTMLElement):
    place: str = Validator(logger=False,
                           debug=True,
                           in_choice=["start", "end", "center", "stretch", "baseline"])

    def __render__(self, elem, place="center"):
        self.place = place
        elem["class"] += f" place-items-{place}"
        return elem


class PlaceSelf(HTMLElement):
    place: str = Validator(logger=False,
                           debug=True,
                           in_choice=["start", "end", "center", "stretch", "auto"])

    def __render__(self, elem, place="center"):
        self.place = place
        elem["class"] += f" place-self-{place}"
        return elem
