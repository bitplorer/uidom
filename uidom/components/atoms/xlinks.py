# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from uidom.dom import *

__all__ = [
    "XLinks",
    "x_links"
]


class XLinks(CustomElement):

    def __render__(self, tag_name):
        return template(div(x_component=tag_name))


x_links = XLinks(tag_name="links")



