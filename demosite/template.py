# Copyright (c) 2023 UiDOM
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from fastapi.templating import Jinja2Templates

from . import settings

templates = Jinja2Templates(settings.webassets.template.dir)

templates.env.globals["DEBUG"] = settings.DEBUG

if settings.DEBUG:
    templates.env.globals["hotreload"] = settings.hot_reload_route
