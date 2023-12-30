# Copyright (c) 2023 UiDOM
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from fastapi.routing import APIRouter

from demosite.document import document
from demosite.pages.nav import ToggleIconsWithoutClickAway, x_nav, x_nav_dependency
from uidom.dom import *
from uidom.routing.fastapi import HTMLRoute, StreamingRoute

header_router = APIRouter(route_class=StreamingRoute)


class IconWrapper(Component):
    def render(self, *args, **kwargs):
        return div(
            *args,
            className="flex items-center justify-center text-center "
            "rotate-90 fill-current overflow-hidden rounded-full "
            "transition-all duration-500 h-5 w-5",
            **kwargs,
        )


x_toggle_nav = ToggleIconsWithoutClickAway(
    tag_name="toggle-nav",
    default_icon=IconWrapper(close_md_icon),
    non_default_icon=IconWrapper(bread_crumb_icon),
)


class Header(XElement):
    def render(self, tag_name):
        with template(x_tagname=tag_name) as _header:
            with div(
                x_data="{open:false, isMed: '', ...$el.parentElement.data()}",
                className="""
                flex md:flex-row flex-col grow mx-auto items-center justify-between px-2 
                shadow-sm shadow-stone-800/40 hover:shadow-md hover:shadow-stone-400/40 
                bg-gray-100 dark:bg-gradient-to-l dark:from-stone-900/90 dark:to-stone-400/80 
                overflow-hidden relative transform transition-all duration-400 p-1 min-w-sm
                """,
            ):
                div(
                    div(
                        x_text="brand",
                        className="""
                        flex grow md:grow-0 font-slim text-2xl items-center justify-center text-center 
                        font-cinzel text-stone-800 dark:text-rose-900/90 overflow-hidden 
                        transition-all duration-400 drop-shadow-lg md:dark:drop-shadow-xl
                        """,
                    ),
                    x_toggle_nav(
                        className="""
                        md:hidden flex justify-center items-center rounded-full
                        text-stone-800 dark:text-stone-100/90
                        """,
                        x_on_click="open = !open",
                        x_on_keydown_dot_escape_dot_window="clicked = true",
                        x_cloak=None,
                    ),
                    className="flex flex-row flex-grow w-full overflow-hidden",
                ),
                div(
                    x_nav(
                        className="""
                        flex flex-row 
                        text-md text-stone-800 dark:text-stone-100/90 
                        overflow-hidden bg-inherit backdrop-blur-xs w-full 
                        origin-top top-13 left-0 h-full font-teko
                        """,
                        x_show="open || isMed",
                        x_init="() => isMed = window.innerWidth > 768;",
                        # x_on_keydown_dot_escape_dot_window="open = false",
                        x_on_resize_dot_window="isMed = window.innerWidth > 768",
                        # x_data="{...$el.parentElement.$data}",
                    ),
                    className="flex grow md:grow-0 w-full md:w-auto ",
                ),

        return _header


x_header = Header(tag_name="header")


@header_router.get("/header")
async def _header():
    with document(
        x_header,
        x_toggle_nav,
        x_nav_dependency,
        head=title("Header Custom Element"),
    ) as head_bar:
        x_header(
            brand="Demosite",
            menu=[
                {
                    "text": "Whole Sellers",
                    "icon": "ant-design:home-outlined",
                    "href": "#_",
                },
                {
                    "text": "Retailers",
                    "icon": "fluent:building-retail-more-20-filled",
                    "href": "#_",
                },
                {"text": "Designers", "icon": "fe:pencil", "href": "#_"},
                {"text": "Manufacturers", "icon": "uil:signout", "href": "#_"},
            ],
            darkmode="true",
        ),
    return head_bar
