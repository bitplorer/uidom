# Copyright (c) 2022 UiDOM
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from dataclasses import dataclass

from fastapi import Form as FForm

from uidom.dom import *

from ..api import api
from ..document import document

__all__ = [
    "x_search"
]


@dataclass
class Search(XComponent):
    icon: dom_tag
    placeholder: str
    target_id: str
    api: str

    def __post_init__(self, *args, **kwargs):
        super(Search, self).__post_init__(
            *args,
            icon=self.icon,
            placeholder=self.placeholder,
            target_id=self.target_id,
            api=self.api,
            **kwargs,
        )

    def render(
        self, *args, tag_name, icon, placeholder, target_id, api, **kwargs
    ):
        return template(
            div(
                div(
                    icon,
                    className="absolute "
                    "flex inset-0 object-contain left-1 top-2 justify-center "
                    "items-center overflow-hidden focus:outline-none m-1 "
                    "h-5 w-5 flex-auto pointer-events-none "
                    "items-center p-0.5 pb-1.5 text-zinc-400 fill-current",
                ),
                input_(
                    name="search_query",
                    type="text",
                    placeholder=placeholder,
                    className="flex flex-row grow w-full form-input "
                    "px-8 border-b-2 border-zinc-200 shadow-md inset-0 "
                    "hover:shadow-lg focus:border-zinc-400 justify-center items-center "
                    "transition-shadow duration-300 focus:outline-none focus:ring-0 "
                    "placeholder:italic placeholder:text-slate-400 overflow-hidden",
                    spellcheck="false",
                    maxlength=64,
                    autocomplete="false",
                    hx_trigger="keyup[target.value.length > 0] changed delay:300ms",
                    hx_target=f"#{target_id}",
                    hx_swap="innerHTML",
                    hx_post=api,
                    x_model="searchText",
                    x_on_input="[(searchText.length > 0) ? show = true : show = false]",
                ),
                div(
                    id=target_id,
                    className="flex flex-row grow justify-center items-center w-full h-screen "
                    "z-10 absolute -left-0.5 top-10 bg-stone-200/40 "
                    "m-0.5 mr-1 backdrop-blur-sm p-2 md:dark:bg-stone-600/10 ",
                    x_on_keydown_dot_escape_dot_window="show = false",
                    x_show="show",
                ),
                className="relative flex flex-col grow h-max w-max justify-between items-center "
                "bg-zinc-100 leading-none text-zinc-500 overflow-hidden",
                x_data="{searchText: '', show: false, ...$el.parentElement.data()}",
                x_cloak=None,
            ),
            x_component=tag_name,
        )


@dataclass
class Search2(XComponent):
    icon: dom_tag
    placeholder: str
    target_id: str
    api: str

    def __post_init__(self):
        super(Search2, self).__post_init__(
            icon=self.icon,
            placeholder=self.placeholder,
            target_id=self.target_id,
            api=self.api,
        )

    def render(self, tag_name, icon, placeholder, target_id, api):
        with template(x_component=tag_name) as search_2:
            with div(x_cloak=None,
                     className="relative flex flex-col grow h-max w-max justify-between items-center "
                               "bg-zinc-100 leading-none text-zinc-500 overflow-hidden rounded-md",
                     x_data="{searchText: '', show: false, ...$el.parentElement.data()}"):
                
                div(icon,
                    className="absolute "
                    "flex inset-0 object-contain left-1 top-2 justify-center "
                    "items-center focus:outline-none m-1 "
                    "h-5 w-5 flex-auto pointer-events-none "
                    "items-center p-0.5 pb-1.5 text-zinc-400 fill-current")

                input_(
                    name="search_query",
                    type="text",
                    placeholder=placeholder,
                    className="flex flex-row grow w-full form-input "
                            "px-8 border-b-2 border-zinc-200 shadow-md inset-0 "
                            "hover:shadow-lg focus:border-zinc-400 justify-center items-center "
                            "transition-shadow duration-300 focus:outline-none focus:ring-0 "
                            "placeholder:italic placeholder:text-slate-400 overflow-hidden rounded-md",
                    spellcheck="false",
                    maxlength=64,
                    autocomplete="false",
                    hx_trigger="keyup[target.value.length > 0] changed delay:800ms",
                    hx_target=f"#{target_id}",
                    hx_swap="innerHTML",
                    hx_post=api,
                    x_model="searchText",
                    x_on_input="[(searchText.length > 0) ? show = true : show = false]",
                ),
                with div(className="h-full w-full overflow-y-auto"):
                    div(id=target_id,
                        className="flex flex-col flex-grow justify-start items-start w-full h-fit "
                                "bg-stone-400/40 m-0.5 p-2 md:dark:bg-stone-600/10 "
                                "shadow-lg shadow-gray-600 overflow-y-auto",
                        x_on_keydown_dot_escape_dot_window="show = false",
                        x_show="show", 
                        x_cloak=None
                        )
            return search_2


x_search = Search2(
    tag_name="search-bar",
    icon=search_icon,
    placeholder="Search",
    target_id="search_results",
    api="/search_api")


@api.get("/search")
def search():
    with document(x_search, head=title("Search Bar")) as search_doc:
        x_search(className="flex w-full")
    return search_doc


last_searched =  []

@api.post("/search_api")
def search_results(search_query: str = FForm(...)):
    global last_searched
    last_searched.append(search_query)
    last_searched = last_searched[-10:]
    if not any(last_searched):
        return div(search_query, className="flex flex-grow w-full h-6 p-2")
    
    with div(className="flex flex-col w-full min-h-96 bg-rose-400 overflow-y-scroll") as _search_data:
        for query in reversed(last_searched):
            div(query, className="flex flex-grow w-full h-24 p-2")
    return _search_data