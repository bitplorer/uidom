# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from uidom import FileSettings, UiDOM, WebAssets
from uidom.dom import XComponentJS, link, script

__all__= ["document"]

document = UiDOM(
    webassets=WebAssets(FileSettings(BASE_DIR=__file__, SUB_DIR="webassets")),
    head=[
        # custom tailwindcss styles sheet
        link(href="/css/styles.css", rel="stylesheet"),
        # google Material Icons
        link(href="https://fonts.googleapis.com/icon?family=Material+Icons&display=block", rel="stylesheet"),
        # Iconify Icons
        script(src="https://code.iconify.design/2/2.1.0/iconify.min.js"),
        # AMP Elements
        script(_async=None, src="https://cdn.ampproject.org/v0.js"),
        # fonts
        link(rel="preconnect", href="https://fonts.googleapis.com"),
        link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=None),
        link(href="https://fonts.googleapis.com/css2?family=Cinzel+Decorative&display=swap", rel="stylesheet"),
        link(href="https://fonts.googleapis.com/css2?family=Teko:wght@300;400;500;600;700&display=swap", rel="stylesheet"),
        link(href="https://fonts.googleapis.com/css2?family=Oswald:wght@500&display=swap", rel="stylesheet"),
        link(href="https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900", rel="stylesheet"),
        link(href="https://fonts.googleapis.com/css2?family=Style+Script&display=swap", rel="stylesheet"),
        ],
    body=[
        # Htmx and Hyperscript
        script(
            src="https://unpkg.com/htmx.org@1.7.0",
            integrity="sha384-EzBXYPt0/T6gxNp0nuPtLkmRpmDBbjg6WmCUZRLXBBwYYmwAUxzlSGej0ARHX0Bo",
            crossorigin="anonymous",
            rel="prefetch"
        ),
        script(src="https://unpkg.com/hyperscript.org@0.8.1"),
        script(defer=None, src="https://unpkg.com/@alpinejs/focus@3.x.x/dist/cdn.min.js"),
        # ALpinejs
        script(src="https://unpkg.com/alpinejs@3.10.2/dist/cdn.min.js", defer=None, rel="prefetch"),
        # livewire
        # script(src="/js/livewire.js"),
        # custom-elements and web component support
        XComponentJS(),
    ]
)
