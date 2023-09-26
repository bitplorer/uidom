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
from uidom import Document
from uidom.dom import Component, script, title, div
from uidom.routing.fastapi import StreamingRoute

document = Document(body=[
    script(src="https://unpkg.com/alpinejs@3.10.2/dist/cdn.min.js", defer=None, rel="prefetch")
    ])

api = FastAPI() 
api.router.route_class = StreamingRoute

class ToggleButton(Component):

    def render(self):
        with div(x_data={'open': 'true'}) as toggle:
            with div(x_on_click='open = !open'):
                div("Opened", x_show="open"), 
                div("Closed", x_show="!open"), 
        return toggle

class App(Component):

    def render(self, *args, **kwargs):
        return document(*args, **kwargs, , head=title('App Page'))


@api.get('/')
def index():
    return App(ToggleButton())

```

## A Jinja template example

```python
from uidom.dom import nav, ul, For, li, a, Var, JinjaElement
from collections import namedtuple as nt


class Nav(JinjaElement):
    def render(self):
        return nav(
            ul(
                For(
                    "item in menu_items",
                    li(a(Var("item.name"), href=Var("item.link"))),
                )
            )
        )

# or we can write Jinja Element directly

Nav = lambda: JinjaElement(nav(ul(For("item in menu_items", li(a(Var("item.name"), href=Var("item.link")))))))

nav_bar = Nav()
menu_url = nt("menu_url", "name link")

# nav_bar element is a jinja template and has an internal representation as follows 
```

```html
<nav>
  <ul>
    {% for item in menu_items %}
      <li>
        <a href="{{ item.link }}">
          {{ item.name }}
        </a>
      </li>
    {% endfor %}
  </ul>
</nav>
```

```python
# now we can use nav_bar just like we use jinja templates and render it as follows

nav_bar(
    menu_items=[
        menu_url("Home", r"\home.html"),
        menu_url("About", r"\about.html"),
        menu_url("Contact Us", r"\contact_us.html"),
    ]
)

# it creates an element as follows
```

```html
<nav>
  <ul>
      <li>
        <a href="\home.html">
          Home
        </a>
      </li>
      <li>
        <a href="\about.html">
          About
        </a>
      </li>
      <li>
        <a href="\contact_us.html">
          Contact Us
        </a>
      </li>
  </ul>
</nav>
```

## using markdown with uidom elements

```python
from uidom.dom import MarkdownElement

em_text = MarkdownElement("*hello world*")

print(em_text)
# it returns following string
```

```html
<p>
  <em>
    hello world
  </em>
</p>
```

```python
# MarkdownElement can be used as follows too 

class HelloWorld(MarkdownElement):
    
    def render(self):
        return "*hello world*"

# now HelloWorld instance gives the same 
# output
print(HelloWorld())
```

```html
<p>
  <em>
    hello world
  </em>
</p>
```

## using raw html with uidom elements

```python
from uidom.dom import *


class Modal(Component):

    def render(self, *args, **kwargs):
        return '''
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
</div>'''

```

## LICENSE

### this library is licensed under MIT (MIT-LICENSE)
