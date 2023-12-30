from apps import settings
from apps.tailwindcss import tailwind
from uidom import Document
from uidom.dom import link, meta, raw, script, uniqueid
from uidom.scripts import html_elements, x_component_js

__all__ = ["document"]


document = Document(
    webassets=settings.webassets,
    head=[
        meta(http_equiv="cache-control", content="no-cache") if settings.DEBUG else "",
        meta(http_equiv="expires", content="0") if settings.DEBUG else "",
        meta(http_equiv="pragma", content="no-cache") if settings.DEBUG else "",
        link(href=f"/css/{tailwind.output_css}?v={next(uniqueid)}", rel="stylesheet"),
        link(
            rel="stylesheet",
            href="https://fonts.googleapis.com/css2?family=Material+Icons+Outlined",
        ),
        link(
            href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300&display=swap",
            rel="stylesheet",
        ),
    ],
    body=[
        script(
            src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js",
            defer=None,
        ),
        script(src="/js/htmx.js"),
        script(
            src=f"/js/{html_elements().save(file_or_dir=settings.webassets.static.js)}"
        ),
        raw(
            settings.hot_reload_route.script()
            if settings.DEBUG and settings.HAS_WEB_SOCK
            else ""
        ),
    ],
)
