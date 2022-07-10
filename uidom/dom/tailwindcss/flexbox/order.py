# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from uidom.dom.htmlelement import HTMLElement


class Order(HTMLElement):

    def __render__(self, elem, order="1"):
        elem["class"] += f" order-{order}"
        return elem


