#!user/bin/env python

# Copyright (c) 2022 uidom
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import uvicorn

from demosite import settings


def run():
    uvicorn.run(
        "demosite.routes:api",
        host="127.0.0.1",
        port=8081,
        reload=settings.DEBUG,
        # ssl_keyfile='../demosite/key.pem',
        # ssl_certfile='../demosite/cert.pem'
    )


if __name__ == "__main__":
    uvicorn.run(
        "routes:api",
        host="127.0.0.1",
        port=8081,
        reload=settings.DEBUG,
        # ssl_keyfile='../demosite/key.pem',
        # ssl_certfile='../demosite/cert.pem'
    )
