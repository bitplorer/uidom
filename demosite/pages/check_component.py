# Copyright (c) 2023 UiDOM
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Union

from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter

from demosite.settings import DEBUG, hot_reload_route
from demosite.tailwindcss import tailwind
from uidom import Document
from uidom.dom import *
from uidom.dom.src.dom_tag import dom_tag
from uidom.dom.src.main import extension
from uidom.routing.fastapi import StreamingRoute
from uidom.scripts import x_component_js_text

testing_api = APIRouter(
    route_class=StreamingRoute,
    default_response_class=HTMLResponse,
    tags=["ALPINE"],
    # include_in_schema=False,
)


@dataclass
class ToggleIconsWithoutClickAway(CustomElement):
    default_icon: dom_tag
    non_default_icon: dom_tag

    def __post_init__(self, *args, **kwargs):
        super(ToggleIconsWithoutClickAway, self).__post_init__(
            *args,
            default_icon=self.default_icon,
            non_default_icon=self.non_default_icon,
            **kwargs,
        )

    def render(self, tag_name, default_icon, non_default_icon):
        with template(x_component=tag_name) as toggele_witout_click_away:
            with div(
                className="flex rounded-full items-center justify-center cursor-pointer",
                x_data={"clicked": "false"},
                x_on_click="clicked = !clicked",
                x_transition_enter="transition ease-in duration-300",
                x_transition_enter_start="opacity-0",
                x_transition_enter_end="opacity-100",
                x_transition_leave="transition ease-in duration-300",
                x_transition_leave_start="opacity-100",
                x_transition_leave_end="opacity-0",
            ):
                button(
                    default_icon,
                    className="flex items-center justify-center text-center rounded-full",
                    x_show="!clicked",
                ),
                button(
                    non_default_icon,
                    className="flex items-center justify-center text-center rounded-full",
                    x_show="clicked",
                )
        return toggele_witout_click_away


x_toggle_dark_mode = ToggleIconsWithoutClickAway(
    tag_name="toggle-dark-mode",
    default_icon=div(
        span(className="iconify", data_icon="teenyicons:bulb-off-solid"),
        # span(data_icon="ic:baseline-light-mode", className="iconify"),
        className="flex h-6 w-6 items-center justify-center",
    ),
    non_default_icon=div(
        span(className="iconify", data_icon="teenyicons:bulb-on-solid"),
        # span(data_icon="ic:baseline-dark-mode", className="iconify"),
        className="flex h-6 w-6 items-center text-yellow-400 justify-center",
    ),
)


@dataclass
class DarkModeButton(XComponent):
    def render(self, tag_name):
        with template(x_component=tag_name) as dark_mode_btn:
            with button(
                className="items-center justify-center overflow-hidden",
            ):
                x_toggle_dark_mode(
                    className="items-center justify-center cursor-pointer",
                    x_data="""{
                    toggle: () => {
                        if (localStorage.theme === 'dark') {
                            localStorage.theme = 'light';
                            document.documentElement.classList.remove('dark');
                        } else {
                            localStorage.theme = 'dark';
                            document.documentElement.classList.add('dark');
                        }
                    },
                }""",
                    x_on_click="toggle",
                    x_init="() => localStorage.theme = 'light'",
                ),

        return dark_mode_btn


x_dark_mode = DarkModeButton(tag_name="dark-mode")


@dataclass
class Navigation(XComponent):
    def __post_init__(self, *args, **kwargs):
        super(Navigation, self).__post_init__(*args, **kwargs)

    def render(self, tag_name):
        with template(x_component=tag_name) as navigation:
            with ul(
                # x_data=None,
                className="flex grow overflow-hidden w-full h-full self-stretch bg-inherit",
            ):
                with template(x_for="item in menu"):
                    with div(
                        className="flex flex-row grow md:grow-0 h-full w-full md:w-fit "
                        "bg-inherit space-x-2 overflow-hidden justify-center items-center "
                        "transform transition duration-400 ease-in ",
                    ):
                        with a(
                            className="flex flex-row grow md:grow-0 items-center justify-center overflow-hidden",
                            x_bind_href="item.href",
                        ):
                            with div(
                                className="flex items-center justify-center text-center",
                            ):
                                with div(
                                    # wrapped menu icon paddings
                                    className="flex md:hidden text-center items-center justify-center px-1 pt-1 sm:pt-0",
                                ):
                                    # Menu Icon
                                    span(
                                        className="iconify",
                                        x_bind_data_icon="item.icon",
                                    ),

                                with div(
                                    # wrapped menu text paddings
                                    className="flex flex-grow pt-1 px-3 items-center justify-center text-center",
                                ):
                                    # Menu text
                                    li(
                                        x_text="item.text",
                                        className="sm:flex hidden grow text-center items-center justify-center "
                                        "whitespace-pre ",
                                    ),

                x_dark_mode(className="flex md:px-3", x_show="darkmode")

        return navigation


x_nav = Navigation(tag_name="nav")
x_nav_dependency = x_toggle_dark_mode & x_nav & x_dark_mode


class IconWrapper(Component):
    def render(self, *args, **kwargs):
        return div(
            *args,
            className="""\
            flex items-center justify-center text-center 
            rotate-90 fill-current overflow-hidden rounded-full 
            transition-all duration-500 h-5 w-5
            """,
            **kwargs,
        )


x_toggle_nav = ToggleIconsWithoutClickAway(
    tag_name="toggle-nav",
    default_icon=IconWrapper(close_md_icon),
    non_default_icon=IconWrapper(bread_crumb_icon),
)


class Header(CustomElement):
    # fields = [("brand", str), ("menu", list), ("darkmode", str)]

    def render(self, tag_name):
        with template(x_component=tag_name) as _header:
            with div(
                x_data={"open": "false", "isMed": ""},
                className="""\
                    flex md:flex-row flex-col grow mx-auto items-center justify-between px-2 
                    shadow-sm shadow-stone-800/40 hover:shadow-md hover:shadow-stone-400/40 
                     bg-gray-100 dark:bg-gradient-to-l dark:from-stone-900/90 dark:to-stone-400/80 
                    overflow-hidden relative transform transition-all duration-400 p-1 min-w-sm
                    """,
            ):
                div(
                    div(
                        x_text="brand",
                        className="""\
                            flex grow md:grow-0 font-slim text-2xl items-center justify-center text-center 
                            font-cinzel text-stone-800 dark:text-rose-900/90 overflow-hidden 
                            transition-all duration-400 drop-shadow-lg md:dark:drop-shadow-xl 
                            """,
                    ),
                    x_toggle_nav(
                        className="""\
                            md:hidden flex justify-center items-center rounded-full
                             text-stone-800 dark:text-stone-100/90 
                             """,
                        x_on_click="open = !open",
                        x_on_keydown_dot_escape_dot_window="clicked = true",
                    ),
                    className="flex flex-row flex-grow w-full overflow-hidden",
                ),
                div(
                    x_nav(
                        className="""\
                            flex flex-row text-md text-stone-800 dark:text-stone-100/90  
                            overflow-hidden bg-inherit backdrop-blur-sm w-full 
                            origin-top top-13 left-0 h-full font-teko 
                            """,
                        x_show="open || isMed",
                        x_init="() => isMed = window.innerWidth > 768;",
                        # x_on_keydown_dot_escape_dot_window="open = false",
                        x_on_resize_dot_window="isMed = window.innerWidth > 768",
                    ),
                    className="flex grow md:grow-0 w-full md:w-auto ",
                ),

        return _header


x_header = Header(tag_name="header")
x_header_dependency = x_nav_dependency & x_toggle_nav & x_header


@testing_api.get("/header_test")
async def _header():
    with document(x_header_dependency, head=title("Header Custom Element")) as head_bar:
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


document = Document(
    head=[
        # custom tailwindcss styles sheet
        link(href=f"/css/{tailwind.output_css}", rel="stylesheet"),
        # google Material Icons
        link(
            href="https://fonts.googleapis.com/icon?family=Material+Icons&display=block",
            rel="stylesheet",
        ),
        # Iconify Icons
        script(src="https://code.iconify.design/2/2.1.0/iconify.min.js"),
        # # AMP Elements
        # script(_async=None, src="https://cdn.ampproject.org/v0.js"),
        # fonts
        link(
            href="https://fonts.googleapis.com/css2?family=Cinzel+Decorative&display=block",
            rel="stylesheet",
        ),
        link(
            href="https://fonts.googleapis.com/css2?family=Teko:wght@300;400;500;600;700&display=block",
            rel="stylesheet",
        ),
        link(
            href="https://fonts.googleapis.com/css2?family=Oswald:wght@500&display=block",
            rel="stylesheet",
        ),
        link(
            href="https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900",
            rel="stylesheet",
        ),
        link(
            href="https://fonts.googleapis.com/css2?family=Style+Script&display=block",
            rel="stylesheet",
        ),
    ],
    body=[
        # Htmx and Hyperscript
        script(
            src="https://unpkg.com/htmx.org@1.8.6/dist/htmx.min.js",
            crossorigin="anonymous",
            rel="prefetch",
        ),
        script(src="https://unpkg.com/hyperscript.org@0.8.1"),
        script(src="https://unpkg.com/htmx.org/dist/ext/preload.js"),
        # livewire
        # script(src="/js/livewire.js"),
        # <!-- Litepicker -->
        script(
            type="text/javascript",
            src="https://cdn.jsdelivr.net/npm/litepicker/dist/litepicker.js",
        ),
        script(
            type="text/javascript",
            src="https://cdn.jsdelivr.net/npm/litepicker/dist/plugins/mobilefriendly.js",
        ),
        # Chart JS
        script(
            src="https://cdn.jsdelivr.net/npm/chart.js",
            # defer=None,
            rel="prefetch",
        ),
        # ALpinejs
        script(
            defer=None,
            src="https://cdn.jsdelivr.net/npm/@alpinejs/focus@3.x.x/dist/cdn.min.js",
        ),
        script(
            src="https://cdn.jsdelivr.net/npm/alpinejs@3.12.0/dist/cdn.min.js",
            defer=None,
            rel="prefetch",
        ),
        # custom-elements and web component support
        script(raw(x_component_js_text())),
        # hot realod the webrowser
        raw(hot_reload_route.script() if DEBUG else ""),
    ],
)

# how to cache a function python ?

if __name__ == "__main__":
    from dataclasses import dataclass, field, make_dataclass
    from typing import Any, Dict, List, Optional

    @dataclass(eq=False)
    class ComponentTags(Component):
        file_extension: str = field(init=False, default=".html")
        render_tag: bool = field(init=False, default=True)
        attributes: dict = field(init=False, default_factory=dict)
        children: List[Union[str, dom_tag]] = field(init=False, default_factory=list)
        parent: Union[dom_tag, None] = field(init=False, default=None)
        document: Union[dom_tag, None] = field(init=False, default=None)

        def __init__(self, *args, **kwargs):
            super(ComponentTags, self).__init__(*args, **kwargs)

        def __checks__(self, element):
            return ...

        def render(self, *args, **kwargs):
            self.add(kwargs)
            self.add(*args)
            return self

    tag_name = "hmm"
    x_tag = make_dataclass(
        cls_name="".join(
            map(
                lambda x: x.capitalize(),
                tag_name.split("-")[1:]
                if tag_name.startswith("x")
                else tag_name.split("-"),
            )
        ),
        fields=[
            ("name", str),
            ("age", int),
            (
                "tagname",
                str,
                field(
                    init=False,
                    default=f"x-{tag_name}"
                    if not tag_name.startswith("x")
                    else tag_name,
                ),
            ),
        ],
        bases=(ComponentTags,),
    )

    class x_tag_2(DoubleTags):
        tagname = f"x-{tag_name}"

    print(x_tag_2(name="bbbb", age=12))
