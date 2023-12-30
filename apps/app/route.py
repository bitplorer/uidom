# Copyright (c) 2023 UiDOM
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from apps.document import document
from apps.tailwindcss import tailwind
from uidom.dom import *
from uidom.elements import *

__all__ = ["get"]


class Button(XElement):
    def render(self, tag_name):
        with template(x_tagname=tag_name, shadowdom=True) as tmpl:
            link(href=f"/css/{tailwind.output_css}", rel="stylesheet")
            button(
                x_data=None, x_text="btn_text", x_cloak=None, x_bind_class="btn_class"
            )
        return tmpl


x_button = Button(tag_name="btn")


async def get():
    """# app"""
    with document() as doc:
        Head(title("Btn"))
        x_button(
            # filename="app/btn.html",
            btn_text="Login",
            btn_class="""flex text-rose-600 text-sm px-2 py-4 items-center justify-center text-center""",
            className="[&:not(:defined)]:opacity-0 transition ease-in duration-[400ms]",
            hx_get="/login",
            hx_target="#content",
        )
        div(id="content", className="flex w-full h-full")

    return doc
