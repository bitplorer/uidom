# Copyright (c) 2022 uidom
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from demosite.api import api
from demosite.document import document
from demosite.pages.modal import Modal

# from demosite.pages.nav import x_nav, x_nav_dependency
from demosite.pages.search import x_search
from demosite.pages.toast import success_toast, x_toast
from uidom.dom import *


@api.get("/")
async def index():
    with document(x_toast, x_search) as page:
        Modal(
            x_search(className="flex w-full"),
            icon=div(search_icon, className="flex px-2 text-stone-400"),
        )
        success_toast("Am Successful Yay!")
    return page
