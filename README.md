<!--
 Copyright (c) 2022 UiDOM
 
 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
-->

# UiDOM

## An HTML library for python

This library is inspired from dominate html library and takes it further. It supports jinja templating and many more features that we expect from an html library. We can even create Custom Elements and Web Components in UiDOM.

## Installation

```cmd
> pip install uidom
```

## An Alpinejs toggle example

```python
#!/usr/bin/env python
# app.py
"""
 This example should work as is. 
"""
from fastapi import FastAPI
from uidom import UiDOM
from uidom.dom import HTMLElement, script, title, div
from uidom.response import doc_response


document = UiDOM(body=[
    script(src="https://unpkg.com/alpinejs@3.10.2/dist/cdn.min.js", defer=None, rel="prefetch")
    ])
api = FastAPI() 


class ToggleMe(HTMLElement):

    def __render__(self):
        return div(
            div(
                div("Opened", x_show="open"), 
                div("Closed", x_show="!open"), 
                x_on_click='open = !open'
            ), 
            x_data={'open': 'true'}
        )


@doc_response
class App(HTMLElement):

    def __render__(self, *args, **kwargs):
        return document(*args, **kwargs, , head=title('App Page'))

@api.get('/')
def index():
    return App(ToggleMe())

```

## A Jinja template example

```python
from uidom.dom import HTMLElement, nav, ul, For, li, a, Var
from jinja2.environment import Template
from collections import namedtuple as nt


class MenuTemplate(HTMLElement):

    def __render__(self):
        return nav(
            ul(
                For(
                    "item in menu_items",
                    li(a(Var("item.name"), href=Var("item.link"))),
                )
            )
        )
# now we can use MenuTemplate just like we use jinja templates and render it 
menu_url = nt("menu_url", "name link")
Template(MenuTemplate.render()).render(menu_items=[
            menu_url("Home", "home.html"),
            menu_url("About", "about.html"),
            menu_url("Contact Us", "contact_us.html")
        ])
```

## using raw html with uidom elements

```python
from uidom.dom import *


class Modal(HTMLElement):

    def __render__(self, *args, **kwargs):
        return HTMLStringToDom('''
<div x-data="{ open: false }">
    <!-- Button -->
    <button x-on:click="open = true" type="button"
        class="px-4 py-2 bg-white border border-black focus:outline-none focus:ring-4 focus:ring-aqua-400">
        Login
    </button>

    <!-- Modal -->
    <div x-show="open" x-on:keydown.escape.prevent.stop="open = false" role="dialog" aria-modal="true"
        x-id="['modal-title']" :aria-labelledby="$id('modal-title')" class="fixed inset-0 overflow-y-auto">
        <!-- Overlay -->
        <div x-show="open" x-transition.opacity class="fixed inset-0 bg-black bg-opacity-50"></div>

        <!-- Panel -->
        <div x-show="open" x-transition x-on:click="open = false"
            class="relative flex items-center justify-center min-h-screen p-4">
            <div x-on:click.stop x-trap.noscroll.inert="open"
                class="relative w-full max-w-2xl p-8 overflow-y-auto bg-white border border-black rounded-md">
               <form wire:submit.prevent="login" action="" class="">
                   <!-- Title -->
                <h2 class="text-3xl font-medium" :id="$id('modal-title')">Confirm</h2>
                <!-- Content -->
                <div class="space-y-3">
                    <div class="">
                        <input wire:model.defer="email" type="email" class="w-full rounded-md">
                    </div>

                    <div class="">
                        <input wire:model.defer="password" type="password" class="w-full rounded-md">
                    </div>
                </div>
                <!-- Buttons -->
                <div class="flex mt-8 space-x-2">
                    <button  type="submit" x-on:click="open = false"
                        class="px-4 py-2 bg-white border border-black focus:outline-none focus:ring-4 focus:ring-aqua-400">
                        Confirm
                    </button>
                    <button type="button" x-on:click="open = false"
                        class="px-4 py-2 bg-white border border-black focus:outline-none focus:ring-4 focus:ring-aqua-400">
                        Cancel
                    </button>
                </div>
               </form>
            </div>
        </div>
    </div>
</div>''').parse()

```

## LICENSE

### this library is licensed under MIT (MIT-LICENSE)
