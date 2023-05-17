# Copyright (c) 2022 uidom
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from demosite import settings
from demosite.tailwindcss import tailwind
from uidom import UiDOM
from uidom.dom import link, raw, script
from uidom.scripts import x_component_js

__all__ = ["document"]


document = UiDOM(
    webassets=settings.webassets,
    head=[
        # custom tailwindcss styles sheet
        link(href=f"/css/{tailwind.output_css}", rel="stylesheet"),
        # google Material Icons
        link(
            href="https://fonts.googleapis.com/icon?family=Material+Icons&display=block",
            rel="stylesheet",
        ),
        # Iconify Icons
        script(src="https://code.iconify.design/2/2.1.0/iconify.min.js"),
        # # AMP Elements
        # script(_async=None, src="https://cdn.ampproject.org/v0.js"),
        # fonts
        link(
            href="https://fonts.googleapis.com/css2?family=Cinzel+Decorative&display=block",
            rel="stylesheet",
        ),
        link(
            href="https://fonts.googleapis.com/css2?family=Teko:wght@300;400;500;600;700&display=block",
            rel="stylesheet",
        ),
        link(
            href="https://fonts.googleapis.com/css2?family=Oswald:wght@500&display=block",
            rel="stylesheet",
        ),
        link(
            href="https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900",
            rel="stylesheet",
        ),
        link(
            href="https://fonts.googleapis.com/css2?family=Style+Script&display=block",
            rel="stylesheet",
        ),
        # ALpinejs
        script(
            defer=None,
            src="https://cdn.jsdelivr.net/npm/@alpinejs/focus@3.x.x/dist/cdn.min.js",
        ),
        script(
            src="https://cdn.jsdelivr.net/npm/alpinejs@3.12.0/dist/cdn.min.js",
            defer=None,
            rel="prefetch",
        ),
        # script(src=settings.alpine_js, defer=None),
    ],
    body=[
        # Htmx and Hyperscript
        script(
            src="https://unpkg.com/htmx.org@1.9.0/dist/htmx.min.js",
            crossorigin="anonymous",
            rel="prefetch",
        ),
        # script(src=settings.htmx_js),
        script(src="https://unpkg.com/hyperscript.org@0.8.1"),
        script(src="https://unpkg.com/htmx.org/dist/ext/preload.js"),
        # livewire
        # script(src="/js/livewire.js"),
        # <!-- Litepicker -->
        script(
            type="text/javascript",
            src="https://cdn.jsdelivr.net/npm/litepicker/dist/litepicker.js",
        ),
        script(
            type="text/javascript",
            src="https://cdn.jsdelivr.net/npm/litepicker/dist/plugins/mobilefriendly.js",
        ),
        # custom-elements and web component support
        # script(x_component_js())
        script(
            src=f"/js/{x_component_js().save(file_or_dir=settings.webassets.static.js / 'component.js')}"
        ),
        # Chart JS
        script(
            src="https://cdn.jsdelivr.net/npm/chart.js",
            # defer=None,
            rel="prefetch",
        ),
        raw(settings.hot_reload_route.script() if settings.DEBUG else ""),
    ],
)
