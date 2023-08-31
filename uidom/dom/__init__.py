# Copyright (c) 2022 uidom
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from .htmlelement import *  # isort: skip
from .htmldocument import *  # isort: skip

from .icons import *  # isort: skip
from .jinja import *  # isort: skip

from .src.component import *
from .src.csstags import *
from .src.ext import *
from .src.htmltags import *
from .src.jinjatags import *
from .src.svgtags import *

from .src.utils import *  # isort: skip
from .src.dom_tag import *  # isort: skip

from .src.html_string import *  # isort: skip
from .uniqueid import *  # isort: skip

# https://github.com/microsoft/vscode/issues/35350#issuecomment-1093627529
# here is the need to include isort skip.
