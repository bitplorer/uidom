# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from uidom.dom import *
from uidom.response import doc_response

from demosite.api import api
from demosite.document import document
from demosite.search import x_search


@doc_response
class App(HTMLElement):

    def __render__(self, *args, **kwargs):
        return document(div(*args, **kwargs))


@api.get('/')
def index():
    return App(x_search(className="flex w-full"), x_search)


