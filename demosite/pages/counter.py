# Copyright (c) 2023 UiDOM
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from dataclasses import dataclass

from fastapi.requests import Request
from valio import IntegerValidator

from demosite.api import api
from demosite.document import document
from uidom.dom import *


class ToggleInset(XComponent):

    def render(self, tag_name):
        return html_string_to_element(f'''
        <template x-component="{tag_name}" >
            <label for="Toggle1" x-data="$el.parentElement.data()" class="inline-flex items-center space-x-4 cursor-pointer dark:text-gray-100">
                <span>Left</span>
                <span class="relative">
                    <input id="Toggle1" type="checkbox" class="hidden peer">
                    <div class="w-10 h-6 rounded-full shadow-inner dark:bg-gray-400 peer-checked:dark:bg-violet-400"></div>
                    <div class="absolute inset-y-0 left-0 w-4 h-4 m-1 rounded-full shadow peer-checked:right-0 peer-checked:left-auto dark:bg-gray-800
                    bg-blue-300 transform"></div>
                </span>
                <span>Right</span>
            </label>
        </template> 
        ''')

@dataclass(eq=False)
class Counter(HTMLElement):
    count: int = IntegerValidator(logger=False, debug=True, default=0)
        
    def __post_init__(self):
        super(Counter, self).__init__(count=self.count)

    def render(self, count):
        with div(
            x_data=None,
            id=f"id_{id(self)}",
            className="block w-1/2 items-center m-2 min-w-fit shadow-lg font-teko bg-stone-50 border border-stone-300 ",
        ) as counter_div:
            div(
                x_text=count,
                className="flex bg-gradient-to-r from-transparent via-stone-600 to-transparent "
                " h-6 w-full text-center text-white text-center "
                "justify-center px-3 ",
            )
            with div(className="inline-flex h-6 w-full mt-2 px-2 "):
                button(
                    "-1",
                    hx_get=f"/decrement/{count}",
                    hx_trigger="click",
                    hx_target=f"#id_{id(self)}",
                    hx_swap="outerHTML",
                    className="flex w-1/2 rounded-l bg-stone-400 text-white text-center "
                    "justify-center items-center hover:bg-stone-600/70 active:bg-stone-600/90 ",
                )
                button(
                    "+1",
                    hx_get=f"/increment/{count}",
                    hx_trigger="click",
                    hx_target=f"#id_{id(self)}",
                    hx_swap="outerHTML",
                    className="flex w-1/2 rounded-r bg-stone-400 text-white text-center "
                    "justify-center items-center hover:bg-stone-600/70 active:bg-stone-600/90 ",
                )
            with div(className="inline-flex h-6 w-full my-2 px-2 font-montserrat"):

                button(
                    "remove",
                    hx_get=f"/remove/{count}",
                    hx_trigger="click",
                    hx_target=f"#id_{id(self)}",
                    hx_swap="outerHTML",
                    className="flex w-1/2 bg-stone-400 text-white text-center "
                    "justify-center items-center hover:bg-stone-600/70 active:bg-stone-600/90 ",
                )
                    
                button(
                    "add",
                    hx_get=f"/add/{count}",
                    hx_trigger="click",
                    hx_target=f"#id_{id(self)}",
                    className="flex w-1/2 rounded-full bg-stone-400 text-white text-center "
                    "justify-center px-3 hover:bg-stone-600/70 active:bg-stone-600/90 mx-2 ",
                    hx_swap="outerHTML",
                )
        return counter_div

    def increment(self):
        self.count += 1
        return self

    def decrement(self):
        if self.count > 0:
            self.count -= 1
        return self

@api.get("/increment/{count}")
async def increment(req: Request, count: int):
    return Counter(count).increment()


@api.get("/decrement/{count}")
async def decrement(req: Request, count: int):
    return Counter(count).increment()


@api.get("/add/{count}")
async def add(req: Request, count: int):
    if "total_count" in req.session:
        total_count = req.session["total_count"] + count
    else:
        total_count = req.session["total_count"] = count

    return div(
        f"{total_count}", 
        id="cart", 
        hx_swap_oob="true", 
        className="rounded-full p-1 bg-rose-300"
        ) & Counter(count=count)


@api.get("/remove/{count}")
async def remove(req: Request, count: int):
    if "total_count" in req.session and req.session["total_count"] >= count:
        reset_counter = req.session["total_count"] - count
    else:
        reset_counter = 0
    removed = Counter(count=reset_counter)
    return div(
        f"{removed.count}", 
        id="cart", 
        hx_swap_oob="true", 
        className="rounded-full p-1 bg-rose-300"
        ) & removed

x_toggle = ToggleInset(tag_name="toggle")


@api.get("/counter")
async def counter(req: Request):
    with document(x_toggle) as counters:
        with div(className="relative flex w-full h-screen"):
            x_toggle(),
            Counter(),
            Counter(count=2) 
            with div(
                className="absolute top-0 right-0 inline-flex items-center justify-center px-2 m-1 space-x-2",
                ):
                span(className="iconify", data_icon="el:shopping-cart")
                div(div("0"), id="cart", className="h-6 w-6 rounded-full font-teko text-lg px-2 text-center bg-teal-300 items-center justify-center"),
    
    return counters
            
        