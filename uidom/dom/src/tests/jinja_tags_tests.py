# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from collections import namedtuple as nt

# import pytest
from uidom.dom.src import Block, For, Var, a, li, nav, render, ul


def block_test():
    menu_url = nt("menu_url", "name link")
    menu = Block(
        "nav",
        nav(
            ul(
                For(
                    "item in menu_items",
                    li(a(Var("item.name"), href=Var("item.link"))),
                )
            )
        ),
    )
    menu_template = menu.render(pretty=True)
    print(menu_template)
    # menu = None
    try:
        menu = render(menu_template,
                      menu_items=[
                          menu_url("Home", "home.html"),
                          menu_url("About", "about.html"),
                          menu_url("Contact Us", "contact_us.html")
                      ]
                      )
        return menu
    except (Exception,) as e:
        menu = e
    if isinstance(menu, Exception):
        return False
    print(menu)


if __name__ == '__main__':
    print(block_test())
