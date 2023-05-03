# Copyright (c) 2023 UiDOM
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from dataclasses import dataclass

from fastapi.requests import Request
from fastapi.websockets import WebSocket
from valio import IntegerValidator

from demosite import settings
from demosite.api import api
from demosite.document import document
from uidom import UiDOM
from uidom.dom import *
from uidom.dom.src.ws_rpc import ws_rpc
from uidom.web_io import (
    EdgeDBFetcher,
    WebSocketAdapter,
    WebSocketClientHandler,
    WebSocketEvents,
)


class ToggleInset(XComponent):
    def render(self, tag_name):
        return string_to_element(
            f"""
        <template x-component="{tag_name}" >
            <label for="Toggle1" x-data="$el.parentElement.data()" class="inline-flex items-center space-x-4 cursor-pointer dark:text-gray-100">
                <span>Left</span>
                <span class="relative">
                    <input _id="Toggle1" type="checkbox" class="hidden peer">
                    <div class="w-10 h-6 rounded-full shadow-inner dark:bg-gray-400 peer-checked:dark:bg-violet-400"></div>
                    <div class="absolute inset-y-0 left-0 w-4 h-4 m-1 transform bg-blue-300 rounded-full shadow peer-checked:right-0 peer-checked:left-auto dark:bg-gray-800"></div>
                </span>
                <span>Right</span>
            </label>
        </template> 
        """
        )


counter_event = WebSocketEvents()


@dataclass(eq=False)
class Counter(ReactiveComponent):
    count: int = IntegerValidator(logger=False, debug=True, default=0)

    def __post_init__(self):
        super(Counter, self).__init__(count=self.count)

    def render(self, count):
        _id = next(uniqueid)
        with div(
            x_data=None,
            hx_boost="true",
            _id=f"id_{_id}",
            className="block w-4/5 items-center m-2 min-w-fit shadow-lg font-teko bg-gray-200 border border-stone-300 ",
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
                    hx_target=f"#id_{_id}",
                    hx_swap="outerHTML",
                    className="flex w-1/2 rounded-l bg-stone-400 text-white text-center "
                    "justify-center items-center hover:bg-stone-600/70 active:bg-stone-600/90 ",
                )
                button(
                    "+1",
                    hx_get=f"/increment/{count}",
                    hx_trigger="click",
                    hx_target=f"#id_{_id}",
                    hx_swap="outerHTML",
                    className="flex w-1/2 rounded-r bg-stone-400 text-white text-center "
                    "justify-center items-center hover:bg-stone-600/70 active:bg-stone-600/90 ",
                    preload="mousedown",
                )
            with div(className="inline-flex h-6 w-full my-2 px-2 font-montserrat"):
                button(
                    "remove",
                    hx_get=f"/remove/{count}",
                    hx_trigger="click",
                    hx_target=f"#id_{_id}",
                    hx_swap="outerHTML",
                    className="flex w-1/2 bg-stone-400 text-white text-center "
                    "justify-center items-center hover:bg-stone-600/70 active:bg-stone-600/90 ",
                )

                button(
                    "add",
                    hx_get=f"/add/{count}",
                    hx_trigger="click",
                    hx_target=f"#id_{_id}",
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

    @counter_event.on_receive("increment")
    def increment_count(self, socket, message):
        self.count += 1
        print("message", message)
        return socket.send(
            str(
                div(
                    self.count,
                    data_event_type="increment_count",
                    data_swap_method="outerHTML",
                    data_payload={},
                )
            )
        )


@api.get("/increment/{count}")
async def increment(req: Request, count: int):
    return Counter(count).increment()


@api.get("/decrement/{count}")
async def decrement(req: Request, count: int):
    return Counter(count).decrement()


@api.get("/add/{count}")
async def add(req: Request, count: int):
    if "total_count" in req.session:
        total_count = req.session["total_count"] + count
    else:
        total_count = req.session["total_count"] = count

    return div(
        f"{total_count}",
        _id="cart",
        hx_swap_oob="true",
        className="rounded-full p-1 bg-rose-300",
    ) & Counter(count=count)


@api.get("/remove/{count}")
async def remove(req: Request, count: int):
    if "total_count" in req.session and req.session["total_count"] >= count:
        reset_counter = req.session["total_count"] - count
    else:
        reset_counter = 0
    removed = Counter(count=reset_counter)
    return (
        div(
            f"{removed.count}",
            _id="cart",
            hx_swap_oob="true",
            className="rounded-full p-1 bg-rose-300",
        )
        & removed
    )


x_toggle = ToggleInset(tag_name="toggle")


@api.get("/counter")
async def counter(req: Request):
    with document(x_toggle) as counters:
        with div(className="relative flex max-w-sm h-screen"):
            Counter()
            # x_toggle(),
            Counter(count=2)
            with div(
                className="absolute top-0 right-0 inline-flex items-center justify-center px-2 m-1 space-x-2",
            ):
                span(className="iconify", data_icon="el:shopping-cart")
                div(
                    div("0"),
                    _id="cart",
                    className="h-6 w-6 rounded-full font-teko text-lg px-2 text-center bg-teal-300 items-center justify-center",
                ),

    return counters


@api.get("/rpc")
async def rpc_check():
    with UiDOM(
        head=link(href="/css/styles.css", rel="stylesheet"),
        body=raw(settings.hot_reload_route.script() if settings.DEBUG else ""),
    )(script(ws_rpc())) as doc:
        div(
            "Counter",
            id="count_test",
            data_event_type="increment_count",
            data_payload="1",
            data_socket="/adapter/counter",
            className="bg-stone-300 bg-opacity-30 w-24 h-10 rounded-md items-center "
            "justify-center text-center font-teko border border-stone-900 shadow-lg shadow-rose-400",
        )

    return doc


ed_fetch = EdgeDBFetcher("efwe")
counter_adapter = WebSocketAdapter(Counter, events=counter_event, data_fetcher=ed_fetch)
sock_handler = WebSocketClientHandler(adapters={"counter": counter_adapter})


@api.websocket("/adapter/{adapter_name}")
async def sockets(websocket: WebSocket, adapter_name: str):
    await sock_handler(websocket=websocket, adapter_name=adapter_name)


if __name__ == "__main__":
    strn = """we will apply the changes only when the render_tag flag is set to True
NOTE: we should **not add** "checks" for (pretty and not self.is_inline) here with
'self_render_tag' as this is where we are adding the indentation and
new-line **before** child is rendered."""

    class xxx(Component):
        def render(self):
            return strn

    print(p(p(strn, x_data={"a": True})))
