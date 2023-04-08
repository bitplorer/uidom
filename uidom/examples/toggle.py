# Copyright (c) 2022 uidom
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from dataclasses import dataclass

from uidom.dom import *

__all__ = ["TogglePlain", "ToggleOutset", "ToggleInset"]


@dataclass
class TogglePlain(AlpineComponent):
    # from https://alpineapple.dev/toggle/

    def render(self, tag_name):
        # "{{'toggle': 'false'}}" <--- how single-quotes ['false', 'toggle'] etc are used
        # to correctly parse f-string
        return f"""
        <div x-data="{{'toggle': 'false'}}" 
            @click="toggle = !toggle" 
            x_component="{tag_name}"
            class="relative w-12 h-6 transition-all duration-300 ease-in-out rounded-full cursor-pointer bg-slate-400" :class=" toggle ? 'bg-cyan-400' : 'bg-slate-400' ">
            <span class="absolute w-6 h-6 transition-all duration-300 ease-in-out bg-white rounded-full" :class=" toggle ? 'translate-x-7' : '' "></span>
        </div>
        """


@dataclass
class ToggleInset(XComponent):
    def render(self, tag_name):
        return f"""
        <template x-component="{tag_name}" >
            <label for="Toggle1" x-data="$el.parentElement.data()" class="inline-flex items-center space-x-4 cursor-pointer dark:text-gray-100">
                <span>Left</span>
                <span class="relative">
                    <input id="Toggle1" type="checkbox" class="hidden peer">
                    <div class="w-10 h-6 rounded-full shadow-inner dark:bg-gray-400 peer-checked:dark:bg-violet-400"></div>
                    <div class="absolute inset-y-0 left-0 w-4 h-4 m-1 rounded-full shadow peer-checked:right-0 peer-checked:left-auto dark:bg-gray-800"></div>
                </span>
                <span>Right</span>
            </label>
        </template>
        """


@dataclass
class ToggleOutset(XComponent):
    def render(self, tag_name):
        return f"""
        <template x-component={tag_name}>
            <label for="Toggle1" class="inline-flex items-center space-x-4 cursor-pointer dark:text-gray-100">
                <span>Left</span>
                <span class="relative">
                    <input id="Toggle1" type="checkbox" class="hidden peer">
                    <div class="w-10 h-6 rounded-full shadow-inner dark:bg-gray-400 peer-checked:dark:bg-violet-400"></div>
                    <div class="absolute inset-y-0 left-0 w-4 h-4 m-1 rounded-full shadow peer-checked:right-0 peer-checked:left-auto dark:bg-gray-800"></div>
                </span>
                <span>Right</span>
            </label>
        </template>
        """


if __name__ == "__main__":
    print(ToggleOutset("xyz")["x-component"])
