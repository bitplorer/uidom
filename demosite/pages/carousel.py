# Copyright (c) 2023 UiDOM
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from demosite.api import api
from demosite.document import document
from uidom.dom import *
from uidom.scripts import x_component_js_text


class carousel(ReactiveComponent):
    def render(self, *args, **kwargs):
        return raw(
            """
                   <div class="flex justify-center">
  <div class="w-full max-w-lg">
    <div class="relative">
      <div class="absolute inset-0 transform skew-x-12 shadow-lg bg-gradient-to-r from-purple-400 via-pink-500 to-red-500"></div>
      <div class="relative z-10 px-4 py-10 bg-white shadow-lg">
        <div class="flex items-center justify-between">
          <button class="p-2 transition duration-200 bg-gray-200 rounded-full hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-400">
            <svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M15 18L9 12L15 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
          <button class="p-2 transition duration-200 bg-gray-200 rounded-full hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-400">
            <svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M9 18L15 12L9 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </div>
        <div class="mt-6">
          <img class="object-cover w-full h-64 rounded-lg shadow-md" src="https://images.unsplash.com/photo-1551963831-b3b1ca40c98e?ixid=MnwxMjA3fDB8MHxzZWFyY2h8M3x8dGltZSUyMHBvbGljeSUyMGNhciUyMGdyYXBoaWNzJTIwZGVzaWduJTIwcmVsZWFzZSUyMGNhcm91c2VsJTIwY2FyZSUyMGJhY2tncm91bmQlMjBzdGF0ZXxlbnwwfHx8fDE2MTk0MjQ2NzQ&ixlib=rb-1.2.1&w=1000&q=80" alt="carousel-image">
        </div>
        <h2 class="mt-6 text-xl font-bold text-gray-800">Carousel Title</h2>
        <p class="mt-2 text-gray-600">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer et elit a risus faucibus suscipit sit amet ut arcu.</p>
        <div class="flex justify-end mt-4">
          <a href="#" class="text-sm font-semibold text-indigo-500 transition duration-200 hover:text-indigo-600">Read more</a>
        </div>
      </div>
    </div>
  </div>
</div>

            """
        )


class CustomElementCheck(XComponent):
    def render(self, tag_name):
        with template(x_component=tag_name) as custom:
            with div(x_data={"name": "bar"}):
                div(x_text="name")
                with div(x_data={"place": "baz"}):
                    div("Place :", div(x_text="place"), className="flex")

            with div(x_data={}):
                div(x_text="name")
            with div(x_data=None):
                div(x_text="name")
        return custom


class Check(HTMLElement):
    def render(self, *args, **kwargs):
        with div(x_data={"name": "root"} | kwargs) as check:
            div(x_text="name")
            with div(x_data={}):
                div(x_text="name", className="flex")
                with div(x_data={"place": "lalalal"}):
                    div("from :", div(x_text="name"), className="flex")

            with div(x_data=None):
                div(x_text="name")

        with div(x_data={"name": "hahah"}):
            div(x_text="name")

        with div(x_data=None):
            div(x_text="name")

        return check


custom_element_check = CustomElementCheck(tag_name="custom-element-check")


@api.get("/name")
def name():
    with document(custom_element_check) as chk:
        custom_element_check(name="foo from parent", place="In")
        Check(name="foo")
    return chk


@api.get("/carousel")
async def carouse():
    return document(carousel())


if __name__ == "__main__":
    print(Check(name="ram"))
