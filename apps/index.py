
from uidom.dom import *
from apps.api import api
from apps.document import document

class Index(Component):
    def render(self, *args, **kwargs):
        return document(*args, **kwargs)

@api.get("/")
def index():
    return Index(div("Hello World"))
    