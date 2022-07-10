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

### An Alpinejs toggle example

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

### A Jinja template example

```python
from uidom.dom import HTMLElement, nav, ul, For, li, a, Var

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
```

## LICENSE

### this library is licensed under MIT (MIT-LICENSE)
