# Copyright (c) 2023 UiDOM
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from collections import namedtuple as nt

from uidom.dom import *


class Nav(JinjaElement):
    def render(self):
        return nav(
            ul(
                For(
                    "item in menu_items",
                    li(a(Var("item.name"), href=Var("item.link"))),
                )
            )
        )


nav_bar = Nav()
menu_url = nt("menu_url", "name link")
nv = nav_bar(
    menu_items=[
        menu_url("Home", r"\home.html"),
        menu_url("About", r"\about.html"),
        menu_url("Contact Us", r"\contact_us.html"),
    ]
)

if __name__ == "__main__":
    em_text = MarkdownElement("~~hello world~~")
    print(em_text)
    # print(nv)
