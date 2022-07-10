# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


import socketserver
from dataclasses import dataclass
from http.server import SimpleHTTPRequestHandler

from uidom.dom import *

PORT = 8000

Handler = SimpleHTTPRequestHandler


@dataclass
class InitializationServer(HTMLElement):

    def __render__(self, *args, **kwargs):
        ...

    def run_server(self, ):
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print("serving at port", PORT)
            httpd.serve_forever()
