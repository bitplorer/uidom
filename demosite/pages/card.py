# Copyright (c) 2023 UiDOM
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import typing as T
from dataclasses import dataclass

from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter

from demosite.document import document
from uidom.dom import *
from uidom.routing import HTMLRoute

card_router = APIRouter(route_class=HTMLRoute, tags=["Card Router"], default_response_class=HTMLResponse)

@dataclass(eq=False)
class BusinessCard(HTMLElement):
    house_name: str | None = None
    city: str | None = None
    
    def __post_init__(self):
        super(BusinessCard, self).__init__(self.house_name, self.city)
    
    def render(
        self,
        house_name=None,
        city=None,
    ):
        with div(className="flex p-2") as _card:
            html_string_to_element(
            f"""
         <div id="app" class="flex bg-white rounded shadow-md w-128 h-60 sm:flex-col text-grey-darkest overflow-hidden">
            <img class="sm:w-fit w-1/2 h-full rounded-l-sm object-cover" src="https://bit.ly/2EApSiC" alt="Room Image">
            <div class="flex flex-col w-full bg-white">
                <div class="flex-1 p-4 pb-0">
                    <h3 class="mb-1 font-light text-grey-900">{house_name or 'Tower Hotel'}</h3>
                    <div class="flex items-center mb-4 text-xs">
                        <i class="mr-1 text-red-900 fas fa-map-marker-alt"></i>
                        {city or 'Soho, London'}
                    </div>
                    <span class="text-5xl text-grey-900">£63.00<span class="text-lg">/PPPN</span></span>
                    <div class="flex items-center mt-4">
                        <div class="pr-2 text-xs">
                            <i class="fas fa-wifi text-green"></i> Free WiFi
                        </div>
                        <div class="px-2 text-xs">
                            <i class="text-grey-darker far fa-building"></i> 2mins to center
                        </div>
                    </div>
                </div>
                <div class="flex items-center justify-between p-3 transition bg-grey-lighter hover:bg-grey-light">
                    Book Now
                    <i class="fas fa-chevron-right"></i>
                </div>
            </div>
        </div>
        """)
        return _card

@card_router.get("/card")
def business_card():
    with document( 
        cls="flex justify-center items-center h-screen w-full bg-gray-600 p-2",
    ) as card:
        for detail in [
            {"city":"Delhi", "house_name": "Raj Bhavan"},
            {"city":"Mumbai", "house_name": "Taj Palace"}
            ]:
            BusinessCard(**detail)
            # BusinessCard(house_name="Lulz", city="Lala Land")
            # BusinessCard(house_name="Lulz", city="Lala Land")
            # BusinessCard(house_name="Lulz", city="Lala Land")
    print(card)
    return card

if __name__ == "__main__":
    print(BusinessCard(house_name="Lulz", city="Lala Land"))
